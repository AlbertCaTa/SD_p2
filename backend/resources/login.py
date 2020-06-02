from Model.artists import ArtistModel
from Model.event import EventModel  # also import table created with many-to-many relationship
from flask_restful import Resource, Api, reqparse

from Model.account import AccountsModel, auth

from flask_httpauth import HTTPBasicAuth
from flask import g

class Login(Resource):
    @auth.login_required(role='admin')
    def get(self):
        accounts = AccountsModel.find_all()
        return {'accounts': list(map(lambda x: x.json(), accounts))}, 200 if accounts else 404

    def post(self):
        data = self.parser()
        acc = AccountsModel.find_by_username(data['username'])
        if not acc:
            return {'message' : 'username not in db'}, 404
        else:
            token = acc.generate_auth_token()
            if acc.verify_password(data["password"]):
                 return {'token': token.decode('ascii')}, 200
            else:
                return {'message': "password invalid"}, 400

    @auth.login_required(role='admin')
    def delete(self):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self):
        return {'message': "Not developed yet"}, 201

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        return data