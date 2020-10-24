"""
Usage
-----

- ``python click_main.py init-db`` to create the database and the ``updates``
  table. Pass the ``--force`` flag to force create the table by first deleting
  it. Optionally, the ``--name`` flag can be used to choose the name of the
  database.
- ``python click_main.py update APP_NAME APP_SIZE`` to add an entry to the
  ``updates`` table in the database. Optionally, the ``--name`` flag can be
  used to choose the database name.
- ``python click_main.py summary`` to see summary statistics of the app
  updates. Optionally, the ``--name`` flag can be used to choose the name of
  the database.

Data Persistence
----------------

The data is persisted in a local sqlite database at the moment, named
``apps_sizes.db`` by default.

The database has a single table, which contains three columns:

- app_name, which is a string column where each entry has length > 0.
- app_size, which is a float column where each entry is > 0.
- update_time, which is a datetime column.

"""
from contextlib import contextmanager
import datetime
import sqlite3

import click

db_name = click.option(
    "--db-name",
    default="apps_sizes.db",
    help="Database name"
)


@click.group()
def cli():
    pass


@cli.command(name="init-db")
@db_name
@click.option(
    "--force/--no-force",
    default=False,
    help="Delete and create the database table",
)
def initialize_database(db_name, force):
    """ Create the database and create an ``updates`` table."""
    conn = sqlite3.connect(db_name)
    if force:
        conn.execute("""DROP TABLE updates""")
    conn.execute(
        """CREATE TABLE updates (name, size, date)"""
    )
    conn.close()


@cli.command(name="update")
@db_name
@click.argument('name')
@click.argument('size')
def update(db_name, name, size):
    """ Add an entry to the database table."""
    with get_db_conn(db_name) as conn:
        conn.execute(
            "INSERT INTO updates VALUES (?, ?, ?)",
            (name, size, datetime.date.today())
        )
        conn.commit()


@cli.command(name="summary")
@db_name
def summary(db_name):
    """ Get summary statistics of entries in the database."""
    with get_db_conn(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECt * FROM updates"
        )
        rows = cursor.fetchall()
    print("\n".join(", ".join(row) for row in rows))


@contextmanager
def get_db_conn(db_name="apps_sizes.db"):
    """ Open and close the connection to a database."""
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()


if __name__ == "__main__":
    cli()
