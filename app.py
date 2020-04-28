from flask import Flask
from flask_restful import Resource, Api, reqparse
from Model.artists import ArtistModel
from Model.event import EventModel  #also import table created with many-to-many relationship
from flask_migrate import Migrate
from db import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)



class Artist(Resource):
    def get(self, id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            return artist.json(), 200
        else:
            return {"message": "Not found"},404

    def post(self, id=None):
        data = self.parser()
        artist = ArtistModel.find_by_id(id)
        if artist:
            return {'message': "Artist with id [{}] already exists".format(id)}, 404
        else:
            artist = ArtistModel(data['name'],data['country'],data['genre'])
            try:
                artist.save_to_db()
            except:
                return {"message": "Error Description"}, 500
            return artist.json(), 201

    def delete(self,id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            artist.delete_from_db(artist)
            return {'message' : 'Artist deleted'}, 200
        else:
            return {'message': "Artist not found"}, 404

    def put(self,id):
        data = self.parser()

        artist = ArtistModel.find_by_id(id)
        if artist:
            artist.delete_from_db()
            artist = ArtistModel(data['name'],data['country'],data['genre'])
            artist.save_to_db()
            return {'message': "Success, artist added"}, 201
        else:
            return {'message' : "Not found"}, 404

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('country', type=str, required=True)
        parser.add_argument('genre', type=str, required=True)

        data = parser.parse_args()
        return data


class Event(Resource):
    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            return event.json(), 200
        else:
            return {"message": "Not found"}, 404

    def post(self, id=None):
        data = self.parser()

        if id and EventModel.find_by_id(id):
            return {'message': "Event with id [{}] already exists".format(id)}, 404
        else:
            event = EventModel(data['name'],data['place'],data['city'],data['date'],data['price'],data['available_tickets'])
            print(event)
            try:
                event.save_to_db()
            except Exception as e:
                print(e)
                return {"message": 'error'}, 500

            return  event.json(), 201

    def delete(self,id):
        event = EventModel.find_by_id(id)
        if event:
            event.delete_from_db()
            return {'message' : 'Event deleted'}, 200
        else:
            return {'message': "Event not found"}, 404

    def put(self,id):
        data = self.parser()
        event = EventModel.find_by_id(id)

        if id and EventModel.find_by_id(id):
            event.delete_from_db()
            event = EventModel(data['place'],data['city'],data['country'],data['date'],data['price'],data['available_tickets'])
            event.save_to_db()
            return {'message': "Success, event added"}, 201
        else:
            return {'message': "Not found"}, 404

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request
        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('place', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('price', type=str, required=True)
        parser.add_argument('available_tickets', type=str, required=True)

        data = parser.parse_args()
        return data

class ArtistList(Resource):
    def get(self):
        artists = ArtistModel.query.all()
        return list(map(lambda x: x.json(), artists)), 200 if artists else 404

    def post(self):
        return {'message': "Not developed yet"}, 201

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 201


class EventList(Resource):
    def get(self):
        events = EventModel.query.all()
        return list(map(lambda x: x.json(), events)), 200 if events else 404

    def post(self):
        return {'message': "Not developed yet"}, 201

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 201


class EventArtistsList(Resource):
    def get(self):
        events = EventModel.query.all()
        return list(map(lambda x: x.json(), events)), 200 if events else 404

    def post(self):
        return {'message': "Not developed yet"}, 201

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 201

class EventArtist(Resource):
    def get(self):
        events = EventModel.query.all()
        return list(map(lambda x: x.json(), events)), 200 if events else 404

    def post(self):
        return {'message': "Not developed yet"}, 201

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 201

class ArtistEventsList(Resource):
    def get(self):
        events = EventModel.query.all()
        return list(map(lambda x: x.json(), events)), 200 if events else 404

    def post(self):
        return {'message': "Not developed yet"}, 201

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 201

api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(ArtistList, '/artists')

api.add_resource(Event, '/event/<int:id>', '/event')
api.add_resource(EventList, '/events')

api.add_resource(EventArtistsList, '/event/<int:id>/artists')
api.add_resource(EventArtist, '/event/<int:id_event>/artist/<id_artist>','/event/<int:id_event>/artist')

api.add_resource(ArtistEventsList, '/artist/<int:id>/events')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

