from user import User
from werkzeug.security import safe_str_cmp

def autenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password) :
        return user

def identity(payload):
    print(payload['identity'])
    user_id = payload['identity']
    return User.find_by_id(user_id)