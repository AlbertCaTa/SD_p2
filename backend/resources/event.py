from models.event import EventModel  # also import table created with many-to-many relationship
from models.account import AccountsModel, auth
from flask_restful import Resource, Api, reqparse

from flask_httpauth import HTTPBasicAuth
from flask import g

class Event(Resource):
    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            return {'event': event.json()}, 200
        else:
            return {"message": "Not found"}, 404

    @auth.login_required(role='admin')
    def post(self, id=None):
        data = self.parser()

        if id and EventModel.find_by_id(id):
            return {'message': "Event with id [{}] already exists".format(id)}, 404
        else:
            event = EventModel(data['name'], data['place'], data['city'], data['date'], data['price'],
                               data['available_tickets'])
            print(event)
            try:
                event.save_to_db()
            except Exception as e:
                print(e)
                return {"message": 'error'}, 500

            return event.json(), 201

    @auth.login_required(role='admin')
    def delete(self, id):
        event = EventModel.find_by_id(id)
        if event:
            event.delete_from_db()
            return {'message': 'Event deleted'}, 200
        else:
            return {'message': "Event not found"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        data = self.parser()
        event = EventModel.find_by_id(id)

        if id and EventModel.find_by_id(id):
            event.delete_from_db()
            event = EventModel(data['name'], data['place'], data['city'], data['date'], data['price'],
                               data['available_tickets'])
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


class EventList(Resource):
    def get(self):
        events = EventModel.find_all()
        return {'events': list(map(lambda x: x.json(), events))}, 200 if events else 404
    @auth.login_required(role='admin')
    def post(self):
        return {'message': "Not developed yet"}, 201

    @auth.login_required(role='admin')
    def delete(self):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self):
        return {'message': "Not developed yet"}, 201
