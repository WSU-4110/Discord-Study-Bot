import mysql.connector


def connection():
    return mysql.connector.connect(user='u244966988_dpy',
                                   password='Qwerty123',
                                   host='sql400.main-hosting.eu',
                                   database='u244966988_discord')


def exec(statement, commit=True):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(statement)
    is_select = statement.split(' ')[0].upper() == "SELECT"  # Adi's special code
    if commit and not is_select:
        conn.commit()
    return cursor.fetchall()