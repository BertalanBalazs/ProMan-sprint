from connection import connection_handler
from psycopg2 import sql
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
def new_board(cursor, boardname, userid):
    cursor.execute("""
    INSERT INTO boards (title,is_active,user_id,status_ids)
    VALUES (%(boardname)s, true ,%(userid)s,'{}')
    RETURNING id as id""",
                   {'boardname': boardname, 'userid': userid})
    return cursor.fetchone()


@connection_handler
def register_new_user(cursor, user_data):
    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (%(username)s , %(hashed_password)s)
        """, user_data)


@connection_handler
def delete_row(cursor, table, criteria):
    cursor.execute(sql.SQL("""
                    DELETE FROM {table}
                    WHERE {col}  = %(value)s
                    """).format(table=sql.Identifier(table), col=sql.Identifier(criteria['key'])), criteria)


@connection_handler
def save_new_status(cursor, title):
    cursor.execute("""
    INSERT INTO statuses (title)
    VALUES (%(title)s)""", {'title': title})


@connection_handler
def get_status(cursor, title):
    cursor.execute("""
    SELECT id FROM statuses WHERE name like %(title)s)""", {'title': title})
    return cursor.fetchone()


@connection_handler
def add_status_to_board(cursor, board_id, status_id):
    status_id = int(status_id)
    cursor.execute("""
    UPDATE boards
     SET status_ids = status_ids || %(status_id)s
    WHERE id = %(board_id)s""", {'board_id': board_id, 'status_id': status_id})


@connection_handler
def save_new_card(cursor, card_data):
    cursor.execute("""
                    INSERT INTO cards (title, board_id, status_id, order_num, user_id)
                    VALUES (%(title)s, %(board_id)s, %(status_id)s, %(order_num)s, %(user_id)s)
                    """,
                   card_data)


@connection_handler
def get_status_for_board(cursor, status_ids):
    cursor.execute("""
                    SELECT * FROM statuses
                    WHERE id in %(status_ids)s
                    """,
                   {'status_ids': tuple(status_ids)})
    return cursor.fetchall()


@connection_handler
def change_status(cursor, new_status):
    cursor.execute("""
                    UPDATE cards
                    SET status_id = %(statusId)s
                    WHERE id = %(id)s
                    """,
                   new_status)


@connection_handler
def rewrite_status_ids(cursor, new_statuses, board_id):
    cursor.execute("""
        UPDATE boards
        SET status_ids = %(new_statuses)s
        WHERE id = %(board_id)s
    """, {'new_statuses': new_statuses, 'board_id': board_id})


@connection_handler
def get_statuses_of_boards(cursor, board_ids):
    cursor.execute(
        '''SELECT boards.id as boardID, s.* FROM boards
            left join boards_statuses bs on boards.id = bs.board_id
            left join statuses s on bs.status_id = s.id
            WHERE boards.id IN %(board_ids)s
            ''', {'board_ids': tuple(board_ids)}
    )
    return cursor.fetchall()


@connection_handler
def get_cards_of_boards(cursor, board_ids):
    cursor.execute('''
        SELECT * from cards
        WHERE board_id IN %(board_ids)s;
''', {'board_ids': tuple(board_ids)})
    return cursor.fetchall()
