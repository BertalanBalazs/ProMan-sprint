import connection


# sample
@connection.connection_handler
def get_boards(cursor, criteria):
    if criteria:
        cursor.execute(f"""
                        SELECT * FROM boards
                        WHERE {criteria['key']} = %(value)s
                        """,
                       criteria)
    else:
        cursor.execute(f"""
                        SELECT * FROM boards
                        """,
                       )
    return cursor.fetchall()
