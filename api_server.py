from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import data_manager
import common

app = Flask(__name__)
app.secret_key = "secret_key"


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


@app.route('/users', methods=['POST'])
def add_new_user():
    data = request.form.to_dict()
    data_manager.register_new_user(data)


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
