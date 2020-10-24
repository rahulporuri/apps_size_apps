"""
Usage
-----

- ``python argparse_main.py --init-db [name.db]`` to initialize the database,
  with the optional argument being the name of the database. By default, the
  database will be named ``apps_sizes.db``.
- ``python argparse_main.py update app_name app_size`` to add an entry in the
  database for ``app_name`` and ``app_size``. Note that in the future, an
  additional commandline argument might be made available to provide time of
  update. At the moment, it is assumed that the update was done on the date
  when the command is executed.
- ``python argparse_main.py statistics`` prints the summary statistics of data
  stored in the database. Specifically, the statistics displayed are:
  - Cumulative app update size for the past week, month and year.
  - Most updated app.
  - Mean and Median app update size.

Data Persistence
----------------

The data is persisted in a local sqlite database at the moment, named
``apps_sizes.db`` by default.

The database has a single table, which contains three columns:

- app_name, which is a string column where each entry has length > 0.
- app_size, which is a float column where each entry is > 0.
- update_time, which is a datetime column.

"""

import argparse
from contextlib import contextmanager
import datetime
import sqlite3


def parse_command_line():
    """ Parse app name and app update size entered by the user.

    Returns
    -------
    args: argparse.NameSpace
        Namespace containing application name and application update size
        as name and size attributes.
    """
    parser = argparse.ArgumentParser(
        description="Store/Retrieve sizes of app updates",
    )
    parser.add_argument(
        'update', nargs='+', help="The name and size of the app being updated",
    )
    parser.add_argument(
        '--init-db', action='store_true', help="Initialize the database",
    )
    return parser.parse_args()


def initialize_database(db_name="apps_sizes.db"):
    """ Initialize the sqlite database if one doesn't exist.
    
    This function connects to the database db_name and creates a table in the
    database with the name ``updates`` which contains three columns:
    - name
    - size
    - date

    """
    conn = sqlite3.connect(db_name)
    conn.execute(
        "create table updates (name, size, date)"
    )
    conn.close()


@contextmanager
def get_db_conn(db_name="apps_sizes.db"):
    """ Get a connection to the database. """
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()


def main():
    """ Entrypoint to the commandline application. """
    args = parse_command_line()
    initialize_database(":memory:")
    app_name, app_size = args.update
    with get_db_conn(":memory:") as conn:
        conn.execute(
            "create table updates (name, size, date)"
        )
        conn.execute(
            "insert into updates values (?, ?, ?)",
            (app_name, app_size, str(datetime.date.today()))
        )
        cursor = conn.cursor()
        cursor.execute(
            "select * from updates"
        )
        print(f"Fetched {cursor.fetchone()} from database.")


if __name__ == "__main__":
    main()
