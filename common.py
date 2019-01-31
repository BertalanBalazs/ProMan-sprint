from flask import jsonify
import data_manager


def delete_from_db(criteria, table):
    try:
        data_manager.delete_row(table, criteria)
    except:
        return jsonify({"done": False, "reason": "Database error"})
    else:
        # if user_id_of_deleted_row == 0:
            # socketio.emit('refresh')
        return jsonify({"done": True, "message": "Successful delete", 'user_id': criteria['value']})


def make_db_query(criteria, table):
    if criteria:
        key = list(criteria.keys())[0]
        value = criteria[key]
        criteria = {"key": key, "value": value}
    try:
        query_result = data_manager.get_data(criteria, table)
    except:
        return jsonify({"done": False, "reason": "Database error"})
    else:
        return jsonify({"done": True, "message": "Successful query", "result": query_result})

