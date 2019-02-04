import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('username',
            type=str,
            required=True,
            help='This field cannot be left blank!'
    )
    parse.add_argument('password',
            type=str,
            required=True,
            help='This field cannot be left blank!'
    )

    def post(self):
        data = UserRegister.parse.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with the username: "{}" already exist'.format(data['username'])}, 400
        user_model = UserModel(**data)
        try:
            user_model.save_to_data()
        except:
            return {"message": 'Internal error'}, 500

        return {'message' : 'User created succesful'}, 201
