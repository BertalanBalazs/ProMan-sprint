from flask import Flask, request, session, jsonify
from flask_cors import CORS
import data_manager
import common
import logging

app = Flask(__name__)
app.secret_key = "secret_key"
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/boards', methods=['GET'])
def get_boards():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'boards')


@app.route('/cards', methods=['GET'])
def get_cards():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'cards')


@app.route('/users', methods=['GET'])
def get_user():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'users')


@app.route('/statuses', methods=['GET'])
def get_status():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'statuses')


@app.route('/boards/<type>', methods=['POST'])
def new_board(type):
    userid = request.form['userid']
    boardtitle = request.form['title']
    try:
        if type == 'public':
            data_manager.new_board(boardtitle, 0)
        else:
            data_manager.new_board(boardtitle, userid)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        return jsonify({'done': True, 'message': 'New board added'})


@app.route('/users', methods=['POST'])
def add_new_user():
    data = request.form.to_dict()
    try:
        data_manager.register_new_user(data)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        return jsonify({'done': True, 'message': 'New user added'})


@app.route('/statuses', methods=['POST'])
def new_status():
    status_title = request.form['title']
    board_id = request.form['boardId']
    board_statuses = data_manager.get_data({'key': 'id', 'value': board_id}, 'boards')[0]['status_ids']
    try:
        if not data_manager.get_data({'key': 'name', 'value': status_title}, 'statuses'):
            data_manager.new_status(status_title)
        status_id = data_manager.get_data({'key': 'name', 'value': status_title}, 'statuses')[0]['id']
        if status_id not in board_statuses:
            data_manager.add_status_to_board(board_id, status_id)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        return jsonify({'done': True, 'message': 'Status added'})


@app.route('/boards/<_id>', methods=['DELETE'])
def delete_board(_id):
    criteria = {'key': 'id', 'value': _id}
    return common.delete_from_db(criteria, 'boards')


@app.route('/cards/<_id>', methods=['DELETE'])
def delete_card(_id):
    criteria = {'key': 'id', 'value': _id}
    return common.delete_from_db(criteria, 'cards')


def main():
    app.run(
        host="127.0.0.1",
        port="8000",
        debug=True
    )


if __name__ == '__main__':
    main()
