from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import requests
import bcrypt

app = Flask(__name__)

app.secret_key = "secret_key"


@app.route("/")
def index():
    ''' this is a one-pager which shows all the boards and cards '''
    if 'username' in session:
        username = {'username': session['username']}
        return render_template('boards.html', username=username, user_id=session.get('userid'))
    return render_template('boards.html')


@app.route('/registration', methods=['GET', 'POST'])
def new_user_registration():
    username = request.form['username']
    response = requests.get('http://127.0.0.1:8000/users', params={'username': username})
    is_username_taken = response.json()['result']
    password = request.form['password']
    password_confirm = request.form['confirm_password']

    if password != password_confirm:
        flash("Password does not match!")
    elif is_username_taken:
        flash("Username is already taken!")
    else:
        flash("Registration was successful!")
        requests.post(
            'http://127.0.0.1:8000/users',
            data={
                "username": username,
                "hashed_password": hash_password(password)
            }
        )
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def log_user_in():
    username = request.form['login_username']
    login_check = False
    password = request.form['login_password']
    response = requests.get('http://127.0.0.1:8000/users', params={"username": username}).json()["result"]
    if response:
        hashed_pw = response[0]["password"]
        login_check = verify_password(password, hashed_pw)


    if login_check:
        session['username'] = username
        session['userid'] = response[0]['id']
    else:
        flash("Invalid Username or Password!")
    return redirect(url_for('index'))


@app.route('/logout')
def log_user_out():
    session.pop('username', None)
    return redirect(url_for('index'))


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    this_was_hashed = plain_text_password
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(this_was_hashed.encode('utf-8'), hashed_bytes_password)


def main():
    app.run(
        host="127.0.0.1",
        port="5000",
        debug=True
    )


if __name__ == '__main__':
    main()
