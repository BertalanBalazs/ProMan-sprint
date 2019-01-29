from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
import data_manager

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    ''' this is a one-pager which shows all the boards and cards '''
    return render_template('boards.html')


@app.route('/boards', methods=['GET'])
def get_boards():
    criteria = request.args.to_dict()
    return make_db_query(criteria, data_manager.get_boards)


def make_db_query(criteria, getter_function):
    if criteria:
        key = list(criteria.keys())[0]
        value = criteria[key]
        criteria = {"key": key, "value": value}
    try:
        query_result = getter_function(criteria)
    except:
        return jsonify({"done": False, "reason": "Database error"})
    else:
        return jsonify({"done": True, "message": "Successful query", "result": query_result})


def main():
    socketio.run(
        app,
        host="0.0.0.0",
        port="8000"
    )


if __name__ == '__main__':
    main()
