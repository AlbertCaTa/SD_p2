from models.event import EventModel  # also import table created with many-to-many relationship
from models.account import AccountsModel, auth
from models.orders import OrdersModel
from flask_restful import Resource, reqparse
from lock import lock
from db import db
from flask import g

class Orders(Resource):
    @auth.login_required(role='user')
    def get(self, username):
        with lock.lock:
            orders = AccountsModel.find_by_username(username).orders
            return {'orders': list(map(lambda x: x.json(), orders))}, 200 if orders else 404

    @auth.login_required(role='user')
    def post(self, username):
        data = self.parser()
        with lock.lock:
            if username == g.user.username:
                a = AccountsModel.find_by_username(username)
                e = EventModel.find_by_id(data['event_id'])
                if e.total_available_tickets >= data["tickets_bought"]:
                    if a.available_money >= e.price * data["tickets_bought"]:
                        e.total_available_tickets = EventModel.total_available_tickets - data["tickets_bought"]
                        a.available_money -= data["tickets_bought"] * e.price
                        o = OrdersModel(e.id, data["tickets_bought"])
                        a.orders.append(o)
                        db.session.commit()
                        return {"order": o.json()}, 201
                    else:
                        return {'message': 'Not enough money'}, 501
                else:
                    return {'message': 'No enough tickets'}, 502
            else:
                return {'message' : 'Endpoint username and g.user.username not equal'}, 400

    @auth.login_required(role='admin')
    def delete(self, username):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self, username):
        return {'message': "Not developed yet"}, 401

    def parser(self):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('event_id', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('tickets_bought', type=int, required=True, help="This field cannot be left blank")

        data = parser.parse_args()
        return data


class OrdersList(Resource):
    @auth.login_required(role='admin')
    def get(self, id):
        with lock.lock:
            orders = OrdersModel.find_all()
            return {'orders': list(map(lambda x: x.json(), orders))}, 200 if orders else 404

    @auth.login_required(role='admin')
    def post(self, id):
        return {'message': "Not developed yet"}, 201

    @auth.login_required(role='admin')
    def delete(self, id):
        return {'message': "Not developed yet"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        return {'message': "Not developed yet"}, 201
