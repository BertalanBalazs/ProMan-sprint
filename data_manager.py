from connection import connection_handler
import bcrypt

# sample
@connection_handler
def get_all_questions(cursor, first_attribute='', second_attribute=''):
    attributes = ['submission_time-DESC', 'submission_time-ASC', 'view_number-DESC',
                  'view_number-ASC', 'vote_number-DESC', 'vote_number-ASC', 'title-DESC', 'title-ASC', '']
    if first_attribute in attributes and second_attribute in attributes:

            SQL_part = 'ORDER BY' if first_attribute or second_attribute else ''
            comma = ', ' if first_attribute and second_attribute else ''
            first_attribute = first_attribute.replace('-', ' ')
            second_attribute = second_attribute.replace('-', ' ')

            cursor.execute(f"""
                            SELECT * FROM question
                            {SQL_part} {first_attribute}{comma}{second_attribute};
                            """)
            return cursor.fetchall()
    else:
        return 'That is not an option.'


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
        """,{'username': username})

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





