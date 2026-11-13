import os
import logging
import argparse
from typing import Any, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error

try:
    from tabulate import tabulate
except ImportError:  # pragma: no cover
    tabulate = None

# ---------------------------------------------------------------------------
# Logger configuration
# ---------------------------------------------------------------------------
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
if not LOGGER.handlers:
    LOGGER.addHandler(handler)

# ---------------------------------------------------------------------------
# Helper to build the MySQL connection arguments from environment variables
# ---------------------------------------------------------------------------
def _build_connection_kwargs() -> dict:
    """Collect connection parameters from environment variables.

    Expected variables:
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
        MYSQL_SSL_CA, MYSQL_SSL_CERT, MYSQL_SSL_KEY (optional SSL files)
    """
    kwargs = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", ""),
    }

    # Include SSL parameters only when all required files are present
    ssl_ca = os.getenv("MYSQL_SSL_CA")
    ssl_cert = os.getenv("MYSQL_SSL_CERT")
    ssl_key = os.getenv("MYSQL_SSL_KEY")
    if all([ssl_ca, ssl_cert, ssl_key]):
        kwargs["ssl_ca"] = ssl_ca
        kwargs["ssl_cert"] = ssl_cert
        kwargs["ssl_key"] = ssl_key
    return kwargs

# ---------------------------------------------------------------------------
# Core query execution function
# ---------------------------------------------------------------------------
def run_query(sql: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple[Any, ...]]:
    """Execute *sql* with optional *params* and return all rows.

    The function establishes a connection using the environment‑derived
    configuration, creates a cursor, runs the query, fetches the results and
    finally closes the cursor and connection.  Errors are logged and re‑raised
    as ``mysql.connector.Error``.
    """
    conn = None
    cursor = None
    try:
        conn_kwargs = _build_connection_kwargs()
        LOGGER.debug("Connecting to MySQL with args: %s", conn_kwargs)
        conn = mysql.connector.connect(**conn_kwargs)
        cursor = conn.cursor()
        LOGGER.info("Executing query: %s", sql)
        cursor.execute(sql, params or ())
        # Use a generator expression to lazily collect rows if needed.
        rows = [row for row in cursor]
        return rows
    except Error as exc:  # pragma: no cover – exercised via integration tests
        LOGGER.error("MySQL error: %s", exc)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            LOGGER.info("MySQL connection closed")

# ---------------------------------------------------------------------------
# Command‑line interface
# ---------------------------------------------------------------------------
def _print_results(rows: List[Tuple[Any, ...]]) -> None:
    """Print *rows* in a human‑readable table.

    If ``tabulate`` is available, it is used for pretty output; otherwise a
    simple column‑wise alignment is performed.
    """
    if not rows:
        print("(no rows returned)")
        return

    headers = [f"col{i+1}" for i in range(len(rows[0]))]
    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        # Plain formatting – determine column widths lazily
        col_widths = [max(len(str(item)) for item in col) for col in zip(*rows, headers)]
        fmt = " | ".join(f"{{:{w}}}" for w in col_widths)
        print(fmt.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
        for row in rows:
            print(fmt.format(*row))

def main() -> None:
    """Entry point for the script.

    Parses a single positional argument ``query`` which is the SQL statement to
    be executed.  The result set is printed to stdout.
    """
    parser = argparse.ArgumentParser(description="Execute a MySQL query and display results.")
    parser.add_argument("query", help="SQL query to execute")
    parser.add_argument(
        "--params",
        nargs="*",
        help="Optional query parameters (as strings); they will be passed to the driver",
    )
    args = parser.parse_args()

    # Convert parameter strings to appropriate Python types lazily using a generator
    params = tuple(args.params) if args.params else None

    try:
        rows = run_query(args.query, params)
        _print_results(rows)
    except Error as exc:
        LOGGER.exception("Failed to execute query")
        # Exit with a non‑zero status code to signal failure
        raise SystemExit(1)

if __name__ == "__main__":
    main()
