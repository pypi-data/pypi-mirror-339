# pgbenchmark

`pgbenchmark` is a Python package to benchmark query performance on a PostgreSQL database. It allows you to measure the
execution time of queries over multiple runs, providing detailed metrics about each run's performance.

## [--- UNDER DEVELOPMENT ---]

## Getting Started

```shell
pip install pgbenchmark
```

---

```python
import psycopg2
from pgbenchmark import Benchmark

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="",
    user="",
    password="",
    host="",
    port=""
)

# Create benchmark instance with desired number of Runs
num_runs = 100_000

# Create a Benchmark class
benchmark = Benchmark(db_connection=conn, number_of_runs=num_runs)

# Set .SQL file to fetch the query from for Benchmark
benchmark.set_sql("./test.sql")

# Or directly pass Raw SQL query
# benchmark.set_sql("SELECT 1;")

# Run the benchmark
benchmark.execute_benchmark()

# Get execution time summary
print("Execution Summary:", benchmark.get_execution_results())

# -----------------------------------------------

# Get execution timeseries using the generator
# (Useful if you want to visualize it as a table.
# "sent_at" is timestamp where `cursor.execute()` was initiated

for execute_data in benchmark.get_execution_timeseries():
    print(execute_data['sent_at'], execute_data['duration'])

```