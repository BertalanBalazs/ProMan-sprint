from flask import Flask, render_template, request, session, redirect, url_for, flash
import data_manager
app = Flask(__name__)


app.secret_key = "secret_key"

@app.route("/")
def boards():
    ''' this is a one-pager which shows all the boards and cards '''
    if 'username' in session:
        username = {'username': session['username']}
        return render_template('boards.html', username=username)
    return render_template('boards.html')


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
    return redirect(url_for('boards'))


@app.route('/login', methods=['POST'])
def log_user_in():
    username = request.form['login_username']
    password = request.form['login_password']

    login_check = data_manager.verify_user(username, password)

    if login_check:
        session['username'] = username
    else:
        pass
    return redirect(url_for('boards'))


@app.route('/logout')
def log_user_out():
    session.pop('username', None)
    return redirect(url_for('boards'))


if __name__ == '__main__':
    main()
