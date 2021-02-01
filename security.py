from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password): #safe_str_cmp does same job as == but good for older versions of python as it takes into account data type like ascii and string etc
        return user

def identity(payload): #here payload is contents of token for authenticating each request accompanied by a token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
