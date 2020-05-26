from Model.event import EventModel
from db import db


class OrdersModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('accounts.username'), nullable=False)
    id_event = db.Column(db.Integer, nullable=False)
    tickets_bought = db.Column(db.Integer, nullable=False)

    def json(self):
        event = EventModel.find_by_id(self.id_event)
        return {
            "Id": self.id_event,
            "Username": self.username,
            "Event_name": event.name,
            "Event_date": event.date,
            "Event_city": event.city,
            "Tickets_bought": self.tickets_bought
        }

    def save_to_db(self):
        if self.id and OrdersModel.query.get(self.id):
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()


    def delete_from_db(self):
        if self.id and OrdersModel.query.get(self.id):
            db.session.delete(self)
            db.session.commit()
        else:
            raise Exception("Warning not in DB")

    @classmethod
    def find_by_username(cls, username):
        if username:
            return OrdersModel.query.filter_by(username=username).all()
        else:
            return None

    @classmethod
    def find_all(cls):
        return OrdersModel.query.all()

    def __init__(self, id_event, tickets_bought):
        self.id_event = id_event
        self.tickets_bought = tickets_bought
