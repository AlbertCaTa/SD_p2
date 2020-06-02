from Model.artists import ArtistModel
from Model.event import EventModel  # also import table created with many-to-many relationship
from Model.account import AccountsModel, auth
from flask_restful import Resource, Api, reqparse

from flask_httpauth import HTTPBasicAuth
from flask import g

class EventArtistsList(Resource):
    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            artists = event.artists
            return {'artists': list(map(lambda x: x.json(), artists))}, 200 if artists else 404
        else:
            return {'message': "Event not found"}, 404
    @auth.login_required(role='admin')
    def post(self, id):
        return {'message': "Not developed yet"}, 201

    @auth.login_required(role='admin')
    def delete(self, id):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        return {'message': "Not developed yet"}, 201


class EventArtist(Resource):
    def get(self, id_event, id_artist):
        event = EventModel.find_by_id(id_event)
        if event:
            artist = next(filter(lambda x: str(x.id) == str(id_artist), event.artists), None)
            if artist:
                return {'artist': artist.json()}, 200 if artist else 404
            else:
                return {'message': "Artist with id [{}] not found".format(id_artist)}, 404
        else:
            return {'message': "Event with id [{}] not found".format(id_event)}, 404

    @auth.login_required(role='admin')
    def post(self, id_event, id_artist=None):
        data = self.parser()
        artist = ArtistModel.find_by_id(id_artist) if id_artist else ArtistModel.find_by_name(data['name'])
        event = EventModel.find_by_id(id_event)
        if not event:
            return {'message': "Event with id [{}] not found".format(id_event)}, 404
        else:
            if not artist:
                artist = ArtistModel(data['name'], data['country'], data['genre'])
                artist.save_to_db()
            try:
                event.artists.append(artist)
                event.save_to_db()
            except:
                return {"message": "Error Description"}, 500

            return {"message": "Success"}, 201

    @auth.login_required(role='admin')
    def delete(self, id_event, id_artist):
        event = EventModel.find_by_id(id_event)
        if event:
            for a in event.artists:
                print("a.id : {}, id_artist: {}, a.id == id_artist: {}".format(a.id,id_artist, a.id == id_artist))
                print("artist {}".format(type(id_artist)))
                print("a {}".format(type(a.id)))
                if a.id == id_artist:
                    event.artists.remove(a)
                    event.save_to_db()
                    return {'message': "Success"}, 200

            return {'message': "Artist with id {} not found".format(id_artist)}, 404
        else:
            return {'message': "Event not found"}, 404

    @auth.login_required(role='admin')
    def put(self, id_event, id_artist):
        return {'message': "Not developed yet"}, 201

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True)
        parser.add_argument('genre', type=str, required=True)

        data = parser.parse_args()
        return data
