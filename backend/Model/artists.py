import json

from db import db

genres = ('REGGAE', 'POP', 'TRAP', 'HIP HOP', 'ROCK', 'INDIE', 'HEAVY', 'ELECTRONIC', 'OTHER')

artist_events = db.Table('artist_events',db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
		db.Column('event_id', db.Integer, db.ForeignKey('event.id')))

class ArtistModel(db.Model):
    __tablename__ = 'artist' #This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.Enum(*genres), nullable=False)
    events = db.relationship('EventModel',secondary=artist_events, backref=db.backref('artists', lazy='dynamic'))

    def __str__(self):
        return str(self.id) + self.name + self.country

    def json(self):
        return {"artist":{"id": self.id,"name": self.name,"country": self.country,"genre": self.genre}}

    @classmethod
    def find_by_id(cls, id):
        if id:
            return ArtistModel.query.get(id)
        else:
            return None

    def save_to_db(self):
        if self.id and ArtistModel.query.get(self.id):
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self):
        if self.id and ArtistModel.query.get(self.id):
            db.session.delete(self)
            db.session.commit()
        else:
            raise Exception("Warning not in DB")

    def __init__(self, name, country, genre):
        self.name = name
        self.country = country
        self.genre = genre
