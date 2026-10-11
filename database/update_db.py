from sqlalchemy import text
from database.db import engine
from datetime import datetime
with engine.begin() as connection:
    columns = connection.execute(
        text("PRAGMA table_info(customers)")
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "balance" not in column_names:
        connection.execute(
            text(
                "ALTER TABLE customers "
                "ADD COLUMN balance FLOAT NOT NULL DEFAULT 5000.0"
            )
        )
        print("Balance column added successfully!")
    else:
        print("Balance column already exists!")
    columns = connection.execute(
        text("PRAGMA table_info(transactions)")
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "created_at" not in column_names:
        connection.execute(
            text(
                "ALTER TABLE transactions "
                "ADD COLUMN created_at DATETIME"
            )
        )
        print("Transaction date column added successfully!")
    else:
        print("Transaction date column already exists!")

from sqlalchemy import text
from database.db import engine
from datetime import datetime

with engine.begin() as connection:
    connection.execute(
        text("""
            UPDATE transactions
            SET created_at = :date
            WHERE created_at IS NULL
        """),
        {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )

print("Missing transaction dates updated!")