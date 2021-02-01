import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser() #not a self variable i.e. it is common to all Item objects
    parser.add_argument('username',
            type = str,
            required = True,
            help = "this field cannot be left blank"
    )
    parser.add_argument('password',
            type = str,
            required = True,
            help = "this field cannot be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'User with this username already exists'}

        user = UserModel(**data) #since data is a dict.
        user.save_to_db()
        return {"message":"user created successfully"}, 201

        