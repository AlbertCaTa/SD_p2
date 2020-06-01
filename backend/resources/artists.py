from Model.artists import ArtistModel
from Model.account import AccountsModel, auth
from flask_restful import Resource, Api, reqparse

from flask_httpauth import HTTPBasicAuth
from flask import g

class Artist(Resource):
    def get(self, id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            return {'artist': artist.json()}, 200
        else:
            return {"message": "Not found"}, 404

    @auth.login_required(role='admin')
    def post(self, id=None):
        data = self.parser()
        artist = ArtistModel.find_by_id(id)
        if artist:
            return {'message': "Artist with id [{}] already exists".format(id)}, 404
        else:
            artist = ArtistModel(data['name'], data['country'], data['genre'])
            try:
                artist.save_to_db()
            except:
                return {"message": "Error Description"}, 500
            return artist.json(), 201

    @auth.login_required(role='admin')
    def delete(self, id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            artist.delete_from_db(artist)
            return {'message': 'Artist deleted'}, 200
        else:
            return {'message': "Artist not found"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        data = self.parser()

        artist = ArtistModel.find_by_id(id)
        if artist:
            artist.delete_from_db()
            artist = ArtistModel(data['name'], data['country'], data['genre'])
            artist.save_to_db()
            return {'message': "Success, artist added"}, 201
        else:
            return {'message': "Not found"}, 404

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True)
        parser.add_argument('genre', type=str, required=True)

        data = parser.parse_args()
        return data


class ArtistList(Resource):
    def get(self):
        artists = ArtistModel.find_all()
        return {'artists': list(map(lambda x: x.json(), artists))}, 200 if artists else 404
    @auth.login_required(role='user')
    def post(self):
        return {'message': "Not developed yet"}, 201

    @auth.login_required(role='admin')
    def delete(self):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self):
        return {'message': "Not developed yet"}, 201