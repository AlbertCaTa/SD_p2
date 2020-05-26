from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import models here
from db import db
from Model.artists import ArtistModel
from Model.event import EventModel
from Model.account import AccountsModel
from Model.orders import OrdersModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

o1=OrdersModel(2,1)
o2=OrdersModel(1,1)
db.session.add(o1)
db.session.add(o2)
db.session.commit()