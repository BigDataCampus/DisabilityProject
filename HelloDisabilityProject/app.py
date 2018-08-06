from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update({'SECRET_KEY':'password'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DisabilityDB.db'
db = SQLAlchemy(app)

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

class Facility(db.Model):
    facilityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_available_name = db.Column(db.String(50),nullable=False)
    facility_is_available = db.Column(db.String(20),nullable=False)
    PlaceID = db.Column(db.Integer,db.ForeignKey("Place.PlaceID"))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/a/<path>')
def goPath(path=None):
    if path:
       return render_template("%s.html" % path)
    else : return 'a'

@app.route('/Place')
def showPlace():
    places = Place.query.all()
    print(places)
    return render_template("show.html", places = places)



if __name__ == '__main__':
    app.run()
