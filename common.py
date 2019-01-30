from flask import jsonify
import data_manager


def delete_from_db(criteria, table):
    try:
        user_id_of_deleted_row = data_manager.delete_row(table, criteria)["user_id"]
    except:
        return jsonify({"done": False, "reason": "Database error"})
    else:
        # if user_id_of_deleted_row == 0:
            # socketio.emit('refresh')
        return jsonify({"done": True, "message": "Successful delete", 'user_id': user_id_of_deleted_row})


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

