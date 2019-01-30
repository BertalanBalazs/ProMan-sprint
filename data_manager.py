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
def new_board(cursor,boardname,userid):
    cursor.execute("""
    INSERT INTO boards (title,is_active,user_id,status_ids)
    VALUES (%(boardname)s, true ,%(userid)s,'{}')""",
                   {'boardname': boardname, 'userid': userid})

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


@connection_handler
def new_status(cursor,title):
    cursor.execute("""
    INSERT INTO statuses (name)
    VALUES (%(title)s)""", {'title': title})



@connection_handler
def get_status(cursor,title):
    cursor.execute("""
    SELECT id FROM statuses WHERE name like %(title)s)""", {'title': title})
    return cursor.fetchone()


@connection_handler
def add_status_to_board(cursor,board_id,status_id):
    status_id = int(status_id)
    cursor.execute("""
    UPDATE boards
     SET status_ids = status_ids || %(status_id)s
    WHERE id = %(board_id)s""", {'board_id': board_id,'status_id': status_id})


@connection_handler
def save_new_card(cursor, card_data):
    cursor.execute("""
                    INSERT INTO cards (title, board_id, status_id, order_num, user_id)
                    VALUES (%(title)s, %(boardId)s, %(statusId)s, %(orderNum)s, %(userId)s)
                    """,
                   card_data)


