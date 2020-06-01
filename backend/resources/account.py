from Model.account import AccountsModel, auth, AVAILABLE_MONEY, IS_ADMIN
from flask_restful import Resource, Api, reqparse

from flask_httpauth import HTTPBasicAuth
from flask import g

class Accounts(Resource):
    def get(self, username):
        account = AccountsModel.find_by_username(username)
        return {'account': account.json()}, 200 if account else 404

    def post(self, username):
        data = self.parser()

        acc = AccountsModel.find_by_username(username)
        if acc:
            return {'message': "username  with id [{}] already exists".format(id)}, 404
        else:
            available_money = data['available_money'] if data["available_money"] else AVAILABLE_MONEY
            is_admin = data['is_admin'] if data["is_admin"]  else IS_ADMIN

            acc = AccountsModel(username, available_money=available_money, is_admin=is_admin)
            acc.hash_password(data['password'])
            acc.save_to_db()

            return {'message' : acc.json()}, 201

        return {'account': acc.json()}, 201

    @auth.login_required(role='user')
    def delete(self, username):
        acc = AccountsModel.find_by_username(username)
        if acc:
            acc.delete_from_db()
            return { 'message' : 'success'}, 201
        else:
            return {'message': "Not in db"}, 404

    @auth.login_required(role='admin')
    def put(self, username):
        return {'message': "Not developed yet"}, 201

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('available_money', type=int)
        parser.add_argument('is_admin', type=int)

        data = parser.parse_args()
        return data

class AccountsList(Resource):
    def get(self):
        accounts = AccountsModel.find_all()
        return {'accounts': list(map(lambda x: x.json(), accounts))}, 200 if accounts else 404

    @auth.login_required(role='admin')
    def post(self):
        return {'message': "Not developed yet"}, 201

    @auth.login_required(role='admin')
    def delete(self):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self):
        return {'message': "Not developed yet"}, 201