from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.username: u for u in users}

# username_mapping = { 'bob' : {
#     'id' : 1,
#     'username' : 'bob',
#     'password' : 'asdf'
# }}
#
# userid_mapping = { 1: {
#     'id' : 1,
#     'username' : 'bob',
#     'password' : 'asdf'
# }}

def authenticate (username, password):
    user = User.find_by_username(username)
    #if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

