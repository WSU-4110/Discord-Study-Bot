import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
_user = os.getenv("DB_USER")
_password = os.getenv("DB_PASS")
_host = os.getenv("DB_HOST")
_database = os.getenv("DB_NAME")


def connection():
    """ create a connection to the database """
    return mysql.connector.connect(user=_user,
                                   password=_password,
                                   host=_host,
                                   database=_database)


def exec(statement, table_name=None, commit=True):
    """ execute a SQL statement in the database and commit the transaction.
    If a table_name is passed in, then the query will be checked for proper completion, returning a boolean """
    conn = connection()
    cursor = conn.cursor(buffered=True)

    if table_name is not None:
        cursor.execute(f"SELECT COUNT(message_id) FROM {table_name}")
        num_before = cursor.fetchall()

    cursor.execute(statement)
    display_keywords = ["SELECT", "DESCRIBE"]
    is_displayable = statement.split(' ')[0].upper() in display_keywords  # Adi's special code

    if not is_displayable:
        if commit:
            conn.commit()
        if table_name is not None:

            statement_kind = statement.split(' ')[0].upper()

            cursor.execute(f"SELECT COUNT(message_id) FROM {table_name}")
            num_after = cursor.fetchall()

            if statement_kind == "INSERT":
                return num_before < num_after
            elif statement_kind == "DELETE":
                return num_before > num_after
            elif statement_kind == "UPDATE":
                return num_before == num_after

    return cursor.fetchall()
