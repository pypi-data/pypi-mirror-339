from pathlib import Path
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor, as_completed
import trino
import os
from datetime import datetime
from tqdm.auto import tqdm
from typing import List, Union, Optional


class DataPipeLine:
    def __init__(self, queries: Union[str, Path, List[Union[str, Path]]]):
        # Convert single query to list
        if not isinstance(queries, list):
            queries = [queries]

        self.queries = [self._process_query(query) for query in queries]
        self.query_sources = {}
        for i, query in enumerate(queries):
            if isinstance(query, Path):
                self.query_sources[i] = f"File {query.stem}"
            else:
                self.query_sources[i] = f"SQL {i + 1}"

        self.prefix = '🤖 TRINO'

    def debug_query(self, index: int = 0):
        if 0 <= index < len(self.queries):
            print(self.queries[index])
        else:
            print(f"Query index {index} is out of range. Available queries: 0-{len(self.queries) - 1}")

    def _process_query(self, query: Union[str, Path]) -> str:
        if isinstance(query, Path):
            with open(str(query), 'r') as f:
                query = f.read()
        return query

    def _time(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def _records_to_df(self, records, columns: list, save_path: Optional[Path] = None):
        # Convert records to DataFrame
        try:
            df = pl.DataFrame(records, orient='row', schema=columns)
            # Convert decimal columns
            col_decimal = [i for i, v in dict(df.schema).items() if v == pl.Decimal]
            if col_decimal:
                df = df.with_columns(pl.col(i).cast(pl.Float64) for i in col_decimal)
        except (pl.exceptions.ComputeError, TypeError) as e:
            print(f'Errors on Polars, switch to Pandas: {e}')
            df = pd.DataFrame(records, columns=columns)

        # Save to file if path provided
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(df, pl.DataFrame):
                df.write_parquet(save_path)
            else:
                df.to_parquet(save_path, index=False, compression='zstd')
            print(f"{self._time()} {self.prefix}: File saved {save_path}")

        return f"Data shape ({df.shape[0]:,.0f}, {df.shape[1]})", df

    def _connection(self):
        username, password, host = (
            os.environ["PRESTO_USER"],
            os.environ["PRESTO_PASSWORD"],
            os.environ["PRESTO_HOST"],
        )
        conn = trino.dbapi.connect(
            host=host,
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        return conn

    def _execute_single_query(
            self,
            query_index: int,
            save_path: Optional[Path] = None,
            verbose: bool = True,
            overwrite: bool = False,
            is_batch: bool = False,
    ) -> Optional[Union[pd.DataFrame, pl.DataFrame]]:

        query = self.queries[query_index]

        # Check if file exists and overwrite is not enabled
        if not overwrite and save_path and save_path.exists():
            print(f"{self._time()} {self.prefix}: {save_path} already exists")
            return None

        # Connect to database
        conn = self._connection()
        cur = conn.cursor()

        # Use tqdm for single query execution, not in batch
        memory = 0
        if verbose and not is_batch:
            thread = ThreadPoolExecutor(1)
            async_result = thread.submit(cur.execute, query)

            pbar = tqdm(total=100, unit="%")
            last_progress = 0

            while not async_result.done():
                try:
                    memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                    state = cur.stats.get('state', 'Not Ready')

                    # Calculate progress percentage
                    progress = 0
                    if state == "RUNNING":
                        completed = cur.stats.get('completedSplits', 0)
                        total = cur.stats.get('totalSplits', 1)  # Avoid division by zero
                        progress = min(99, int((completed / total) * 100)) if total > 0 else 0

                    # Update progress bar
                    if progress > last_progress:
                        pbar.update(progress - last_progress)
                        last_progress = progress

                    pbar.set_description(f"{self.prefix} Single thread {state} - Memory {memory:.1f}GB")
                except Exception as e:
                    tqdm.write(f"Error updating progress: {e}")

            pbar.update(100 - last_progress)
            pbar.close()
        else:
            try:
                cur.execute(query)
                memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
            except Exception as e:
                print(f"{self._time()} {self.prefix}: Error executing #{query_index}: {e}")
                return None

        print(f"{self._time()} {self.prefix}: Fetching #{query_index} Memory {memory:.1f}GB")
        try:
            records = cur.fetchall()
            columns = [i[0] for i in cur.description]
            text, df = self._records_to_df(records, columns, save_path)

            print(f"{self._time()} {self.prefix}: #{query_index} {text}")
            return df
        except Exception as e:
            print(f"{self._time()} {self.prefix}: #{query_index}: {e}")
            return None

    def run_presto_to_df(
            self,
            save_paths: Optional[List[Path]] = None,
            verbose: bool = True,
            overwrite: bool = False,
            max_concurrent: int = 3,
    ):
        if save_paths is None:
            save_paths = [None] * len(self.queries)
        elif not isinstance(save_paths, list):
            save_paths = [save_paths]

        if len(save_paths) != len(self.queries):
            error_message = f"# save paths ({len(save_paths)}) must match # queries ({len(self.queries)})"
            raise ValueError(error_message)

        # Single query case
        if len(self.queries) == 1:
            result = self._execute_single_query(0, save_paths[0], verbose, overwrite)
            return result

        # Multiple queries case
        print(f"{self._time()} {self.prefix}: Running {len(self.queries)} queries in {max_concurrent} threads")
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(
                    self._execute_single_query, i, save_paths[i], verbose, overwrite, True
                ): i for i in range(len(self.queries))
            }

            # Process results as they complete
            for future in tqdm(as_completed(future_to_index), desc=f"{self.prefix} Multi Threads",total=len(future_to_index)):
                query_index = future_to_index[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"{self._time()} {self.prefix} Error processing query {query_index}: {e}")

    def run_batch(
            self,
            save_dir: Optional[Path] = None,
            file_prefix: str = "raw",
            verbose: bool = True,
            overwrite: bool = False,
            max_concurrent: int = 3,
    ):
        save_paths = None
        if save_dir:
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
            save_paths = [save_dir / f"{file_prefix}_{i}.parquet" for i in range(len(self.queries))]

        results = self.run_presto_to_df(save_paths, verbose, overwrite, max_concurrent)

        if not isinstance(results, list):
            # Single result case
            return results


# Run multiple queries
# pipeline = DataPipeLine([query1])
# results_dict = pipeline.run_batch(save_dir=Path("./query_results"), max_concurrent=2)
