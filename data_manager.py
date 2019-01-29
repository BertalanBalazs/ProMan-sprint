from connection import connection_handler
import bcrypt


# sample
@connection_handler
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


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    this_was_hashed = plain_text_password
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(this_was_hashed.encode('utf-8'), hashed_bytes_password)


@connection_handler
def register_new_user(cursor, username, password):
    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (%(username)s , %(hashed_password)s)
        """, {'username': username, 'hashed_password': hashed_password})


@connection_handler
def verify_user(cursor, username, password):
    cursor.execute("""
        SELECT password FROM users
        WHERE username=%(username)s;
        """, {'username': username})

    hashed_password_dict = cursor.fetchall()
    hashed_password = hashed_password_dict[0]['password']

    if len(hashed_password) == 0:
        return False
    else:
        pw_check = verify_password(password, hashed_password)
        return pw_check


@connection_handler
def check_username_in_database(cursor, username):
    cursor.execute("""
        SELECT * FROM users
        WHERE username=%(username)s;
        """, {'username': username})
    username = cursor.fetchall()

    if len(username) == 0:
        return False
    else:
        return True


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
def add_status_to_board(board_id,status_id):
    cursor.execute("""
    UPDATE boards
     SET status_ids status_ids || %(status_id)s
    WHERE id LIKE (%(board_id)s)""", {'board_id': board_id,'status_id': status_id})



