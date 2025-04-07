"""Utility functions"""

import json
from pathlib import Path
import sqlite3
from typing import List, Literal, Tuple
from rich import print


def get_database_name(database: Path) -> str:
    """
    Returns the database name.

    Args:
        database (Path): Database file path

    Returns:
        str: Database name
    """

    return (
        database.name
        if database.name.endswith((".sqlite3", ".db"))
        else database.name + ".sqlite3"
    )


def execute_sql_script(database: sqlite3.Connection, script: str) -> None:
    """
    Executes a SQL script.

    Args:
        database (sqlite3.Connection): Database connection
        script (str): SQL script string
    """

    database.cursor().executescript(script)
    database.commit()


def execute_sql_file(database: sqlite3.Connection, path: Path) -> None:
    """
    Executes a SQL file.

    Args:
        database (sqlite3.Connection): Database connection
        file (str): SQL script filename
    """

    with open(path, "r", encoding="utf-8") as file:
        execute_sql_script(database, file.read())


def create_initial_schema(database: sqlite3.Connection) -> None:
    """
    Creates the initial schema to insert Quran text.

    Args:
        name (str): Database filename
    """

    print("Creating [bold]the initial schema[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "schemas" / "initial.sql",
    )
    print("[bold green]Done[/bold green]")


def create_views(database: sqlite3.Connection) -> None:
    """
    Creates views to help with data access.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Creating [bold]the views[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "schemas" / "views.sql",
    )
    print("[bold green]Done[/bold green]")


def insert_initial_data(database: sqlite3.Connection) -> None:
    """
    Inserts the Quran text into the database

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Inserting [bold]initial data[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "data" / "verses.sql",
    )
    print("[bold green]Done[/bold green]")


def create_normalized_schema(database: sqlite3.Connection) -> None:
    """
    Creates the normalized schema to normalize the initial database.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Creating [bold]the normalized schema[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "schemas" / "normalized.sql",
    )
    print("[bold green]Done[/bold green]")


def insert_chapters(
    database: sqlite3.Connection, with_diacritics: bool = False
) -> None:
    """
    Insert chapters (Al-Suwar) data into the database.

    Args:
        database (sqlite3.Connection): Database connection
        with_diacritics (bool): Weather to include arabic diacritics in chapter names
    """

    print("Inserting [bold]chapters[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "data" / "chapters.sql",
    )

    if with_diacritics:
        with open(
            Path(__file__).parent / "assets" / "data" / "chapters.json",
            encoding="utf-8",
        ) as f:
            for c in json.load(f):
                database.cursor().execute(
                    'UPDATE "chapters" SET "name" = ? WHERE "id" = ?',
                    (c["new_name"], c["id"]),
                )

    print("[bold green]Done[/bold green]")


def get_verse(
    database: sqlite3.Connection,
    chapter_id: int,
    verse_number: int,
) -> Tuple[int, int, int, str]:
    """
    Get a verse by chapter id and verse number.

    Args:
        database (sqlite3.Connection): Database connection
        chapter_id (int): Chapter ID
        verse_number (int): Verse number

    Returns:
        Tuple[int, int, int, str]: Tuple with the verse data
    """

    return (
        database.cursor()
        .execute(
            "SELECT * FROM quran WHERE chapter_id = ? AND number = ?",
            (chapter_id, verse_number),
        )
        .fetchone()
    )


def get_verse_range(
    database: sqlite3.Connection,
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> Tuple[int, int]:
    """
    Get the verse range as (start_verse_id, end_verse_id).

    Args:
        database (sqlite3.Connection): Database connection
        start (Tuple[int, int]): Start chapter_id and verse_number
        end (Tuple[int, int]): End chapter_id and verse_number

    Returns:
        Tuple[int, int]: Tuple with the start and end verse ids
    """

    return (
        get_verse(database, start[0], start[1])[0],
        get_verse(database, end[0], end[1])[0] - 1,
    )


def get_table_verse_range(
    database: sqlite3.Connection,
    table: Literal["parts", "pages", "quarters"],
) -> List[Tuple[int, int]]:
    """
    Get verse ranges for each part, quarter and page as (start_verse_id, end_verse_id).
    The index of the item in the returned list represents the id of the part, quarter or page.

    Args:
        database (sqlite3.Connection): Database connection
        table (str): Table name

    Returns:
        List[Tuple[int, int]]: Verse range representation of each item in the list.
    """

    with open(
        Path(__file__).parent / "assets" / "data" / "metadata.json",
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)[table]

        res = []
        for index, item in enumerate(data):
            if index < len(data) - 1:
                res.append(get_verse_range(database, item, data[index + 1]))
            else:
                res.append((res[-1][1] + 1, 6236))

        return res


def insert_verses(database: sqlite3.Connection) -> None:
    """
    Insert verses (Al-Aayat) data into the database.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Inserting [bold]verses[/bold]...", end=" ")
    execute_sql_script(
        database,
        'INSERT INTO "verses" ("number", "content", "chapter_id") '
        'SELECT "number", "content", "chapter_id" FROM "quran";',
    )
    print("[bold green]Done[/bold green]")


def insert_table_data(database: sqlite3.Connection) -> None:
    """
    Insert data into parts, groups, quarters and pages tables.

    Args:
        database (sqlite3.Connection): Database connection

    Returns:
        bool: True if the data is inserted successfully else False.
    """

    print(
        "Inserting data into [bold]parts, groups, quarters and pages tables[/bold]...",
        end=" ",
    )

    cursor = database.cursor()

    for i in range(1, 31):
        cursor.execute("INSERT INTO parts (name) VALUES (?)", (f"Part {i}",))

    for i in range(1, 61):
        cursor.execute("INSERT INTO groups (name) VALUES (?)", (f"Group {i}",))

    for i in range(1, 241):
        cursor.execute("INSERT INTO quarters (name) VALUES (?)", (f"Quarter {i}",))

    for i in range(1, 605):
        cursor.execute("INSERT INTO pages (name) VALUES (?)", (f"Page {i}",))

    database.commit()

    print("[bold green]Done[/bold green]")


def set_verse_fks(database: sqlite3.Connection) -> None:
    """
    Update the verses table to set part_id, group_id, quarter_id and page_id.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print(
        "Updating [bold]verses[/bold] table to set "
        "[bold]part_id, group_id, quarter_id and page_id[/bold]...",
        end=" ",
    )

    cursor = database.cursor()

    tables = ["parts", "pages", "quarters"]
    for table in tables:
        data = get_table_verse_range(database, table)

        for i, item in enumerate(data, start=1):
            cursor.execute(
                f'UPDATE "verses" SET "{table[:-1]}_id" = ? where "id" between ? AND ?',
                (i, *item),
            )

        database.commit()

    # Insert group data
    data = get_table_verse_range(database, "quarters")
    ahzab = [
        (data[i][0], data[i + 3][1] if i + 4 < len(data) - 1 else 6236)
        for i in range(0, 240, 4)
    ]

    for i, item in enumerate(ahzab, start=1):
        cursor.execute(
            'UPDATE "verses" SET group_id = ? where "id" between ? AND ?',
            (i, *item),
        )

    database.commit()
    print("[bold green]Done[/bold green]")


def set_verse_count(database: sqlite3.Connection) -> None:
    """
    Update corresponding tables to set verse_count.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Setting [bold]verse_count[/bold]...", end=" ")

    cursor = database.cursor()

    tables = ["groups", "parts", "quarters", "pages"]
    for table in tables:
        data = cursor.execute(
            f'SELECT COUNT(*) FROM "verses" GROUP BY "{table[:-1]}_id"'
        ).fetchall()

        for i, item in enumerate(data, start=1):
            cursor.execute(
                f'UPDATE {table} SET "verse_count" = ? WHERE "id" = ?', (item[0], i)
            )

    database.commit()

    print("[bold green]Done[/bold green]")


def set_page_count(database: sqlite3.Connection) -> None:
    """
    Update corresponding tables to set page_count.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Setting [bold]page_count[/bold]...", end=" ")

    cursor = database.cursor()

    tables = ["chapters", "parts", "groups", "quarters"]
    for table in tables:
        data = cursor.execute(
            f'SELECT COUNT(DISTINCT "pages"."id") FROM "pages" INNER JOIN "verses" ON '
            f'("pages"."id" = "verses"."page_id") GROUP BY "verses"."{table[:-1]}_id"'
        ).fetchall()

        for i, item in enumerate(data, start=1):
            cursor.execute(
                f'UPDATE {table} SET "page_count" = ? WHERE "id" = ?', (item[0], i)
            )

    database.commit()

    print("[bold green]Done[/bold green]")


def set_foreign_keys(database: sqlite3.Connection) -> None:
    """
    Update groups, quarters and pages tables to set foreign keys.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print(
        "Setting foreign keys for [bold]groups, quarters and pages tables[/bold]...",
        end=" ",
    )

    cursor = database.cursor()

    tables = [
        {
            "name": "groups",
            "select": 'SELECT "part_id" FROM "verses" GROUP BY "group_id"',
            "update": 'UPDATE "groups" SET "part_id" = ? WHERE "id" = ?',
        },
        {
            "name": "quarters",
            "select": 'SELECT "part_id", "group_id" FROM "verses" GROUP BY "quarter_id"',
            "update": 'UPDATE "quarters" SET "part_id" = ?, "group_id" = ? WHERE "id" = ?',
        },
        {
            "name": "pages",
            "select": 'SELECT "chapter_id", "part_id", "group_id", "quarter_id" FROM "verses" GROUP BY "page_id"',
            "update": 'UPDATE "pages" SET "chapter_id" = ?, "part_id" = ?, "group_id" = ?, "quarter_id" = ? WHERE "id" = ?',
        },
    ]

    for table in tables:
        data = cursor.execute(table["select"]).fetchall()

        for item in enumerate(data, start=1):
            cursor.execute(table["update"], (*item[1], item[0]))

    database.commit()

    print("[bold green]Done[/bold green]")


def insert_interpretations(database: sqlite3.Connection) -> None:
    """
    Insert interpolations (Tafsir) data into the database.

    Args:
        database (sqlite3.Connection): Database connection
    """

    print("Inserting [bold]interpolations[/bold]...", end=" ")
    execute_sql_file(
        database,
        Path(__file__).parent / "assets" / "data" / "test.sql",
    )
    print("[bold green]Done[/bold green]")
