from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from resources.artists import ArtistList, Artist
from resources.event import EventList, Event
from resources.orders import OrdersList, Orders
from resources.eventArtist import EventArtist, EventArtistsList
from resources.artistEvents import ArtistEventsList
from resources.account import Accounts, AccountsList
from resources.login import Login

from flask_migrate import Migrate
from flask import render_template
from db import db, secret_key



app = Flask(__name__,
            static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")

app.config.from_object(__name__)

api = Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def render_vue():
    return render_template("index.html")


# TODO fix html return codes.


api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(ArtistList, '/artists')

api.add_resource(Event, '/event/<int:id>', '/event')
api.add_resource(EventList, '/events')

api.add_resource(EventArtistsList, '/event/<int:id>/artists')
api.add_resource(EventArtist, '/event/<int:id_event>/artist/<id_artist>', '/event/<int:id_event>/artist')

api.add_resource(ArtistEventsList, '/artist/<int:id>/events')

api.add_resource(Orders, '/orders/<string:username>')
api.add_resource(OrdersList, '/orders')

api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
