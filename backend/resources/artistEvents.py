from models.artists import ArtistModel
from models.account import AccountsModel, auth
from flask_restful import Resource, Api, reqparse

class ArtistEventsList(Resource):
    @auth.login_required(role='admin')
    def get(self, id):
        events = ArtistModel.find_by_id(id).events
        return {'events': list(map(lambda x: x.json(), events))}, 200 if events else 404

    @auth.login_required(role='admin')
    def post(self, id):
        return {'message': "Not developed yet"}, 401

    @auth.login_required(role='admin')
    def delete(self, id):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        return {'message': "Not developed yet"}, 401