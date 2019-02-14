from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import data_manager
import common
import logging

app = Flask(__name__)
app.secret_key = "secret_key"
CORS(app)
socketio = SocketIO(app)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/boards', methods=['GET'])
def get_boards():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'boards')


@socketio.on('load-data')
def socketio_get_boards():
    boards = data_manager.get_data({}, 'boards')
    socketio.emit('load-data', boards)

@app.route('/cards', methods=['GET'])
def get_cards():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'cards')


@app.route('/users', methods=['GET'])
def get_user():
    criteria = request.args.to_dict()
    return common.make_db_query(criteria, 'users')


@app.route('/statuses/<board_id>', methods=['GET'])
def get_status(board_id):
    statuses = data_manager.get_data({'key': 'id', 'value': board_id}, 'boards')[0]['status_ids']
    if statuses:
        return jsonify(
            {'done': True, 'message': 'Successful query', 'result': data_manager.get_status_for_board(statuses)})
    else:
        return jsonify({'done': True, 'message': 'Successful query', 'result': {}})


@app.route('/boards/<type>', methods=['POST'])
def new_board(type):
    userid = request.get_json()['userid']
    boardtitle = request.get_json()['title']

    try:
        if type == 'public':
            board_id = data_manager.new_board(boardtitle, 0)['id']
        else:
            board_id = data_manager.new_board(boardtitle, userid)['id']
    except:
        return jsonify({'done': False, 'message': 'Database error', 'result': board_id})
    else:
        socketio.emit('boardlist-change')
        return jsonify({'done': True, 'message': 'New board added', 'result': board_id})


@socketio.on('add-board')
def socketio_new_board(message):
    userid = message['userid']
    boardtitle = message['title']
    data_manager.new_board(boardtitle, userid)['id']
    socketio.emit('boardlist-change')


@app.route('/cards', methods=['POST'])
def create_card():
    card_data = request.get_json()
    try:
        data_manager.save_new_card(card_data)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        socketio.emit('board-change')

        return jsonify({'done': True, 'message': 'New card added'})


@socketio.on('add-card')
def socketio_create_card(message):
    data_manager.save_new_card(message)
    socketio.emit('board-change')


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
def save_new_status():
    status_title = request.get_json()['title']
    board_id = request.get_json()['boardId']
    board_statuses = data_manager.get_data({'key': 'id', 'value': board_id}, 'boards')[0]['status_ids']
    try:
        if not data_manager.get_data({'key': 'title', 'value': status_title}, 'statuses'):
            data_manager.save_new_status(status_title)
        status_id = data_manager.get_data({'key': 'title', 'value': status_title}, 'statuses')[0]['id']
        if status_id not in board_statuses:
            data_manager.add_status_to_board(board_id, status_id)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        socketio.emit('board-change')
        return jsonify({'done': True, 'message': 'Status added', 'result': status_id})


@socketio.on('add-status')
def socketio_save_new_status(message):
    status_title = message['title']
    board_id = message['boardId']
    board_statuses = data_manager.get_data({'key': 'id', 'value': board_id}, 'boards')[0]['status_ids']
    if not data_manager.get_data({'key': 'title', 'value': status_title}, 'statuses'):
        data_manager.save_new_status(status_title)
    status_id = data_manager.get_data({'key': 'title', 'value': status_title}, 'statuses')[0]['id']
    if status_id not in board_statuses:
        data_manager.add_status_to_board(board_id, status_id)
    socketio.emit('board-change')


@app.route('/cards/<id_>', methods=['PATCH'])
def change_status(id_):
    new_status = request.get_json()
    new_status['id'] = int(id_)
    try:
        data_manager.change_status(new_status)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        socketio.emit('board-change')
        return jsonify({'done': True, 'message': 'Status changed'})


@socketio.on('change-status')
def socket_change_status(message):
    data_manager.change_status(message)
    socketio.emit('board-change')


@app.route('/boards/<_id>', methods=['DELETE'])
def delete_board(_id):
    criteria = {'key': 'id', 'value': _id}
    socketio.emit('boardlist-change')
    return common.delete_from_db(criteria, 'boards')


@socketio.on('delete-board')
def socketio_delete_board(message):
    criteria = {'key': 'id', 'value': message['id']}
    common.delete_from_db(criteria, 'boards')
    socketio.emit('boardlist-change')


@app.route('/cards/<_id>', methods=['DELETE'])
def delete_card(_id):
    criteria = {'key': 'id', 'value': _id}
    socketio.emit('board-change')

    return common.delete_from_db(criteria, 'cards')


@socketio.on('delete-card')
def socketio_delete_card(message):
    criteria = {'key': 'id', 'value': message['card_id']}
    common.delete_from_db(criteria, 'cards')
    socketio.emit('board-change')


@app.route('/boards/<_id>/<status_id>', methods=['DELETE'])
def delete_status(_id, status_id):
    criteria = {'key': 'id', 'value': _id}
    statuses = data_manager.get_data(criteria, 'boards')[0]['status_ids']
    statuses.remove(int(status_id))
    data_manager.delete_row('cards', {'key': 'status_id', 'value': status_id})
    try:
        data_manager.rewrite_status_ids(statuses, _id, status_id)
    except:
        return jsonify({'done': False, 'message': 'Database error'})
    else:
        socketio.emit('board-change')
        return jsonify({'done': True, 'message': 'Status deleted'})


@socketio.on('delete-column')
def socketio_delete_status(message):
    criteria = {'key': 'id', 'value': message['board_id']}
    statuses = data_manager.get_data(criteria, 'boards')[0]['status_ids']
    statuses.remove(int(message['column_id']))
    data_manager.delete_row('cards', {'key': 'status_id', 'value': message['column_id']})
    data_manager.rewrite_status_ids(statuses, message['board_id'], message['column_id'])
    socketio.emit('board-change')


@socketio.on('refresh-request')
def socketio_get_statuses(board_ids):
    if board_ids:
        boards_statuses = data_manager.get_statuses_of_boards(board_ids)
        boards_cards = data_manager.get_cards_of_boards(board_ids)
        socketio.emit('refresh-response', {'board_ids': board_ids, 'statuses': boards_statuses, 'cards': boards_cards})


def main():
    socketio.run(
        app,
        host="127.0.0.1",
        port="8000",
        debug=True
    )


if __name__ == '__main__':
    main()
