from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import data_manager

app = Flask(__name__)


app.secret_key = "secret_key"

@app.route("/")
def index():
    ''' this is a one-pager which shows all the boards and cards '''
    if 'username' in session:
        username = {'username': session['username']}
        return render_template('boards.html', username=username)
    return render_template('boards.html')


@app.route('/boards', methods=['GET'])
def get_boards():
    criteria = request.args.to_dict()
    return make_db_query(criteria, data_manager.get_boards)


@app.route('/boards', methods=['DELETE'])
def delete_board():
    criteria = request.form.to_dict()
    return delete_from_db(criteria, 'boards')


@app.route('/cards', methods=['DELETE'])
def delete_card():
    criteria = request.form.to_dict()
    return delete_from_db(criteria, 'cards')


def delete_from_db(criteria, table):
    if criteria:
        key = list(criteria.keys())[0]
        if key != 'id':
            return jsonify({"done": False, "reason": f"Rows can be deleted from {table} only via id"})
        value = criteria[key]
        criteria = {"key": key, "value": value}
    else:
        return jsonify({"done": False, "reason": f"It is not specified, which row has to be deleted from {table}"})
    try:
        user_id_of_deleted_row = data_manager.delete_row(table, criteria)["user_id"]
    except:
        return jsonify({"done": False, "reason": "Database error"})
    else:
        # if user_id_of_deleted_row == 0:
            # socketio.emit('refresh')
        return jsonify({"done": True, "message": "Successful delete"})



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
    app.run(debug=True)


@app.route('/registration', methods=['GET', 'POST'])
def new_user_registration():
    username = request.form['username']

    is_username_taken = data_manager.check_username_in_database(username)
    password = request.form['password']
    password_confirm = request.form['confirm_password']

    if password != password_confirm:
        flash("Password does not match!")
    elif is_username_taken:
        flash("Username is already taken!")
    else:
        flash("Registration was successful!")
        data_manager.register_new_user(username,password)
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def log_user_in():
    username = request.form['login_username']
    password = request.form['login_password']

    login_check = data_manager.verify_user(username, password)

    if login_check:
        session['username'] = username
    else:
        pass
    return redirect(url_for('index'))


@app.route('/logout')
def log_user_out():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    main()
