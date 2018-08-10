from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import json


app = Flask(__name__)
app.config.update({'SECRET_KEY':'password'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DisabilityDB.db'
db = SQLAlchemy(app)

admin = Admin(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Place(db.Model):
    placeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(20), nullable=False)
    place_address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.FLOAT, nullable=False)
    lng = db.Column(db.FLOAT, nullable=False)
    category = db.Column(db.String(20), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'placeID':self.placeID,
            'place_name':self.place_name,
            'place_address' : self.place_address,
            'lat' : self.lat,
            'lng' : self.lng,
            'category' : self.category
        }

class Facility(db.Model):
    facilityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_available_name = db.Column(db.String(50),nullable=False)
    facility_is_available = db.Column(db.String(20),nullable=False)
    PlaceID = db.Column(db.Integer,db.ForeignKey("Place.PlaceID"))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Place, db.session))
admin.add_view(ModelView(Facility, db.session))

@app.route('/')
def index():
    return render_template('index-2.html')


@app.route('/<path>')
def goPath(path=None):
    if path:
       return render_template("%s" % path)
    else : return 'a'

@app.route('/Place')
def showPlace():
    places = Place.query.all()
    print(places)
    return render_template("show.html", places = places)

@app.route('/listing')
def PlaceSetting():
    places = Place.query.all()
    print("pp",places)
    json_list = [i.serialize for i in places]
    print(json_list)
    return render_template('base2.html', places = json_list)

if __name__ == '__main__':
    app.run()
