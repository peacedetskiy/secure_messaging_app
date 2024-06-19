import bcrypt
import jwt
from db import get_db
from config import APP_SECRET


def register(name, password):
    db = get_db()
    cursor = db.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    cursor.execute('INSERT INTO "user"(name, password, salt) VALUES (%s, %s, %s)',
                   (name, hashed_password.decode('utf-8'), salt.decode('utf-8')))
    db.commit()


def login(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT TRIM(name), password, salt FROM "user" WHERE name = %s', (username,))
    user = cursor.fetchone()
    if user:
        user_name, stored_password, stored_salt = user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), stored_salt.encode('utf-8')).decode('utf-8')
        if hashed_password == stored_password:
            return user_name
    return False


def check_user(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT TRIM(name) FROM "user" WHERE name = %s', (username,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


def decode_token(token):
    try:
        token_payload = jwt.decode(token, APP_SECRET, algorithms=['HS256'])
        return token_payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
    except jwt.InvalidSignatureError:
        return {'error': 'Invalid token'}


def get_user_from_token(request):
    token = request.headers.get('Cookie')
    if not token:
        return False
    jwt_token_index = token.find('jwt_token')
    if jwt_token_index == -1:
        return False
    jwt_token_find = token[jwt_token_index:].split('=')[1].split(';')[0]
    decoded_token = decode_token(jwt_token_find)
    if 'error' in decoded_token:
        return decoded_token
    if check_user(decoded_token['name']):
        return decoded_token['name']
    else:
        return False
