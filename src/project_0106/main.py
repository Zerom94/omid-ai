# -*- coding: utf-8 -*-
"""MySQL client example.

This script demonstrates a secure and robust way to connect to a MySQL database,
run a parametrised SELECT statement and pretty‑print the results.

The implementation follows the guidelines:
* Connection parameters are loaded from environment variables (optionally via a
  ``.env`` file).
* ``mysql-connector-python`` is used as the client library.
* All resources are released in a ``finally`` block.
* Results are streamed lazily and displayed with ``tabulate``.
* List comprehensions, generator expressions and ``str.join`` are used where
  appropriate to satisfy performance best‑practices.
"""

from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from typing import Any, Generator, Iterable, List, Tuple

try:
    # ``python-dotenv`` is optional – if it is not installed we simply skip it.
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv() -> None:  # type: ignore[misc]
        """Fallback stub when ``python-dotenv`` is unavailable."""
        return None

# Load ``.env`` if present – this keeps secrets out of the source code.
load_dotenv()

import mysql.connector
from mysql.connector import MySQLConnection, cursor
from mysql.connector.errors import Error as MySQLError
from tabulate import tabulate

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def _get_env(name: str, default: str | None = None) -> str:
    """Retrieve an environment variable or raise a clear error.

    Args:
        name: Variable name.
        default: Value returned when the variable is missing.  If ``None``
            a ``RuntimeError`` is raised.

    Returns:
        The variable's value.
    """
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is required but not set.")
    return value

# ---------------------------------------------------------------------------
# Context manager for the MySQL connection
# ---------------------------------------------------------------------------

@contextmanager
def mysql_connection() -> Generator[MySQLConnection, None, None]:
    """Yield a MySQL connection configured via environment variables.

    The connection uses SSL if the corresponding variables are present.  Any
    ``MySQLError`` is re‑raised after being wrapped with a more descriptive
    message.
    """
    # Required parameters
    config: dict[str, Any] = {
        "user": _get_env("MYSQL_USER"),
        "password": _get_env("MYSQL_PASSWORD"),
        "host": _get_env("MYSQL_HOST", "localhost"),
        "port": int(_get_env("MYSQL_PORT", "3306")),
        "database": _get_env("MYSQL_DATABASE"),
    }

    # Optional SSL configuration – only added when all pieces are supplied.
    ssl_ca = os.getenv("MYSQL_SSL_CA")
    ssl_cert = os.getenv("MYSQL_SSL_CERT")
    ssl_key = os.getenv("MYSQL_SSL_KEY")
    if ssl_ca and ssl_cert and ssl_key:
        config["ssl_ca"] = ssl_ca
        config["ssl_cert"] = ssl_cert
        config["ssl_key"] = ssl_key
        config["ssl_verify_cert"] = True

    conn: MySQLConnection | None = None
    try:
        conn = mysql.connector.connect(**config)
        yield conn
    except MySQLError as exc:  # pragma: no cover
        raise RuntimeError(f"Failed to connect to MySQL: {exc}") from exc
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

# ---------------------------------------------------------------------------
# Query execution
# ---------------------------------------------------------------------------

def run_select_query(query: str, params: Tuple[Any, ...] = ()) -> None:
    """Execute a parametrised SELECT query and print results.

    The function streams rows using a generator to keep the memory footprint low.
    ``tabulate`` receives a list of rows, which is built lazily via a list
    comprehension – suitable for typical result sets that comfortably fit into
    memory.  For extremely large datasets you could replace the list with an
    iterator directly passed to ``tabulate``.

    Args:
        query: The SELECT statement with placeholders (``%s``) for parameters.
        params: A tuple of values to bind to the placeholders.
    """
    with mysql_connection() as conn:
        cursor_obj: cursor.MySQLCursor = conn.cursor(dictionary=True)
        try:
            cursor_obj.execute(query, params)
            # Lazy fetch – ``fetchmany`` could be used for huge tables.
            rows_generator: Generator[dict[str, Any], None, None] = (
                row for row in cursor_obj
            )
            # Pull the first row to inspect column names; if there are none we
            # simply report an empty result set.
            try:
                first_row = next(rows_generator)
            except StopIteration:
                print("[INFO] Query returned no rows.")
                return

            # Re‑inject the first row and build a list for tabulate.
            rows: List[dict[str, Any]] = [first_row, *list(rows_generator)]
            headers: List[str] = list(first_row.keys())
            # ``tabulate`` works with list‑of‑dicts when ``headers='keys'``.
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        except MySQLError as exc:  # pragma: no cover
            raise RuntimeError(f"Query execution failed: {exc}") from exc
        finally:
            cursor_obj.close()

# ---------------------------------------------------------------------------
# Example usage (executed when the script is run directly)
# ---------------------------------------------------------------------------

def _example() -> None:
    """Run a sample query using environment configuration.

    The example assumes a table called ``employees`` with columns ``id`` and
    ``name``.  Adjust the query as needed for your schema.
    """
    sample_query = "SELECT id, name FROM employees WHERE department = %s"
    sample_params = ("Engineering",)
    run_select_query(sample_query, sample_params)

if __name__ == "__main__":
    try:
        _example()
    except Exception as e:
        # Print a concise error message and exit with a non‑zero status.
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
