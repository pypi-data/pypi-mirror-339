"""Normalize command"""

from pathlib import Path
import sqlite3
from typing import Annotated
import typer
from rich import print

from quran_cli import utils


def normalize(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database file"),
    ],
    diacritics: Annotated[
        bool,
        typer.Option(
            "-d",
            "--with-diacritics",
            help="Weather to include Arabic diacritics in chapter names",
        ),
    ] = False,
) -> None:
    """
    Normalize initial Quran database.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3

    quran-cli normalize db.sqlite3
    ```
    """

    try:
        connection = sqlite3.connect(database)

        print(f"Normalizing [bold]{database}[/bold]...")

        utils.create_normalized_schema(connection)
        utils.insert_chapters(connection, diacritics)
        utils.insert_verses(connection)
        utils.insert_table_data(connection)
        utils.set_verse_fks(connection)
        utils.set_verse_count(connection)
        utils.set_foreign_keys(connection)
        utils.set_page_count(connection)
        utils.create_views(connection)

        connection.close()

        print("Normalization [bold green]completed[/bold green].")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
