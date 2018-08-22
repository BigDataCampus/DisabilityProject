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
    place_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(20), nullable=False)
    place_address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.FLOAT, nullable=False)
    lng = db.Column(db.FLOAT, nullable=False)
    category = db.Column(db.String(20), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'place_ID':self.place_ID,
            'place_name':self.place_name,
            'place_address' : self.place_address,
            'lat' : self.lat,
            'lng' : self.lng,
            'category' : self.category
        }

class Facility(db.Model):
    facility_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_available_name = db.Column(db.String(50),nullable=False)
    facility_is_available = db.Column(db.String(20),nullable=False)
    Place_ID = db.Column(db.Integer,db.ForeignKey("Place.Place_ID"))

    @property
    def serialize(self):
        return {
            'facility_ID':self.facility_ID,
            'facility_available_name':self.facility_available_name,
            'facility_is_available':self.facility_is_available,
            'place_ID':self.Place_ID
        }

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
def place_Setting():
    content = request.args.get("content")
    print("ccc:",content)
    if content :
        places = Place.query.filter(Place.place_name.like('%'+content+'%'))
    else :
        places = Place.query.all()
    json_list = [i.serialize for i in places]
    return render_template('base2.html', places = json_list)


@app.route('/getData')
def getData():
    data = request.args.get('a')
    fac = Facility.query.filter_by(Place_ID=data)
    f = [i.serialize for i in fac]
    return json.dumps(f)


@app.route('/listings-single/<place_id>')
def place_SingleListing(place_id):
    info = Place.query.filter_by(place_ID=place_id)
    facinfo = Facility.query.filter_by(Place_ID = place_id)

    return render_template("listings-single-page.html", info = info.all(), facinfo = facinfo.all())
if __name__ == '__main__':
    app.run()











