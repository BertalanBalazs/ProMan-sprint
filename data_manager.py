from connection import connection_handler
import bcrypt

# sample
@connection_handler
def get_data(cursor, criteria, table):
    if criteria:
        cursor.execute(f"""
                        SELECT * FROM {table}
                        WHERE {criteria['key']} = %(value)s
                        """,
                       criteria)
    else:
        cursor.execute(f"""
                        SELECT * FROM {table}
                        """,
                       )
    return cursor.fetchall()


@connection_handler
def register_new_user(cursor, user_data):
    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (%(username)s , %(hashed_password)s)
        """, user_data)


@connection_handler
def delete_row(cursor, table, criteria):
    cursor.execute(f"""
                    DELETE FROM {table}
                    WHERE id = %(value)s
                    RETURNING user_id
                    """,
                   criteria)
    return cursor.fetchone()
