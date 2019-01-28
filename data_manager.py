import connection


# sample
@connection.connection_handler
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
