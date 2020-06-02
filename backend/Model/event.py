import json
from db import db


class EventModel(db.Model):
    __tablename__ = 'event' #This is table name
    __table_args__ = (db.UniqueConstraint('name', 'date', 'city'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    place = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_available_tickets = db.Column(db.Integer, nullable=False)


    def __str__(self):
        return str(self.id) + self.name + self.city

    def json(self):
        return {
                "id": self.id,
                "name": self.name,
                "place": self.place,
                "city": self.city,
                "date": self.date,
                "price": self.price,
                "total_available_tickets": self.total_available_tickets,
                'artists' : list(map(lambda x: x.json(), list(self.artists)))
        }

    def save_to_db(self):
        if self.id and EventModel.query.get(self.id):
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self):
        if  self.id and EventModel.query.get(self.id):
            db.session.delete(self)
            db.session.commit()
        else:
            raise Exception("Warning not in DB")

    @classmethod
    def find_by_id(cls, id):
        if id:
            return EventModel.query.get(id)
        else:
            return None

    @classmethod
    def find_all(cls):
        return EventModel.query.all()

    def add_artist(self, modelArtist):
        self.artists.append(modelArtist)

    def __init__(self, name, place, city, date, price, total_available_tickets):
        self.name = name
        self.place = place
        self.city = city
        self.date = date
        self.price = price
        self.total_available_tickets = total_available_tickets
