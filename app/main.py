import secrets
import jwt
import datetime
from flask import Flask, request, make_response, render_template, redirect, url_for, session, abort
from flask_cors import CORS
from auth import register, login, get_user_from_token, check_user
from message import send_message, get_messages
from config import APP_SECRET, JWT_SECRET_KEY, JWT_TOKEN_LOCATION


app = Flask(__name__)
app.secret_key = APP_SECRET
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = [JWT_TOKEN_LOCATION]
CORS(app=app)


@app.route('/')
def index():
    user = get_user_from_token(request=request)
    if not user:
        print('No token provided')
        return redirect(url_for('user_login'))
    elif 'error' in user:
        print('Error in token')
        return redirect(url_for('user_login'))
    else:
        return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        password = data['password']
        if check_user(name):
            return '<h1>User already registered.</h1>'
        if len(name) > 30 or len(name) == 0:
            return '<h1>Your username is too long or too short.</h1>'
        register(name, password)
        response = make_response(redirect(url_for('index')), 201)
        return response
    else:
        return render_template('auth.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user_name = login(name, password)
        if user_name:
            token = jwt.encode({
                "name": user_name,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            }, APP_SECRET, algorithm='HS256')
            response = make_response(redirect(url_for('index')))
            response.set_cookie('Cookie', f'jwt_token={token}', httponly=True, secure=True, max_age=3600)
            return response
        else:
            return '<h1>Invalid user or password.</h1>'
    else:
        return render_template("auth.html")


@app.route('/message', methods=['GET', 'POST'])
def message_send():
    if request.method == 'POST':
        data = request.form
        sender = get_user_from_token(request=request)
        if not sender:
            return '<h1>Unauthorized. Please log in.</h1>'
        if 'error' in sender:
            return '<h1>Oops! Troubles with logging you in.</h1><h2>Please log in again</h2>'
        recipient = data['recipient']
        content = data['content']
        if not check_user(recipient):
            return '<h1>Invalid message or recipient.</h1>'

        message_sent = send_message(sender, recipient, content)
        if message_sent:
            return redirect(url_for('message_list'))
        else:
            return '<h1>Invalid message or recipient.</h1>'
    else:
        return render_template("send_message.html")


@app.route('/messages', methods=['GET'])
def message_list():
    caller = get_user_from_token(request=request)
    if not caller:
        return '<h1>Unauthorized access.</h1><h2>You are logged out or token has expired. Please log in.</h2>'
    elif 'error' in caller:
        return '<h1>Oops! Troubles with logging you in.</h1><h2>Please log in again</h2>'
    messages = get_messages(caller=caller)
    if messages:
        return render_template("messages.html", messages=messages)
    else:
        return render_template("messages.html", messages=None)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        response = make_response(redirect(url_for('user_login')))
        response.set_cookie('Cookie', '', expires=0, httponly=True, secure=True)
        session.clear()
        return response
    else:
        return render_template('logout.html')


def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


@app.before_request
def csrf_protect():
    if request.method == 'POST':
        token = session.pop('csrf_token', None)
        if not token or token != request.form.get('csrf_token'):
            abort(403)


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context="adhoc")
