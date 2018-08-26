from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)
app.config.update({'SECRET_KEY':'password'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DisabilityDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    json_list = [i.serialize for i in places]
    return render_template('base2.html', places = json_list)

@app.route('/listings-single')
def PlaceSingleListing():
    place_id = request.args.get('place_ID')
    info = Place.query.filter_by(place_ID=place_id)
    facinfo = Facility.query.filter_by(Place_ID = place_id)

    return render_template("listings-single-page.html", info = info.all(), facinfo = facinfo.all())


@app.route('/test')
def test():

    return jsonify({'x':['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구',
       '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구',
       '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'],
                    'y' : [2777, 1855,  952, 2243, 1460,  950, 1111, 1376, 1754, 1228,  745,
       1026, 1006, 1051, 1697,  908, 1202, 3199,  910, 1343,  814, 1331,
       1197,  902, 1130],
                    } )


@app.route('/get_place')
def get_place():
    return jsonify({'x1':['강남구',
                          '강동구',
                          '강북구',
                          '강서구',
                          '관악구',
                          '광진구',
                          '구로구',
                          '금천구',
                          '노원구',
                          '도봉구',
                          '동대문구',
                          '동작구',
                          '마포구',
                          '서대문구',
                          '서초구',
                          '성동구',
                          '성북구',
                          '송파구',
                          '양천구',
                          '영등포구',
                          '용산구',
                          '은평구',
                          '종로구',
                          '중구',
                          '중랑구'],
                    'y1': [631,
                          461,
                          213,
                          582,
                          368,
                          209,
                          238,
                          309,
                          399,
                          309,
                          183,
                          247,
                          237,
                          244,
                          414,
                          222,
                          396,
                          624,
                          239,
                          323,
                          208,
                          476,
                          286,
                          235,
                          271],
                    'x2': ['종로구',
                         '중구',
                         '용산구',
                         '성동구',
                         '광진구',
                         '동대문구',
                         '중랑구',
                         '성북구',
                         '강북구',
                         '도봉구',
                         '노원구',
                         '은평구',
                         '서대문구',
                         '마포구',
                         '양천구',
                         '강서구',
                         '구로구',
                         '금천구',
                         '영등포구',
                         '동작구',
                         '관악구',
                         '서초구',
                         '강남구',
                         '송파구',
                         '강동구'],
                    'y2':[6064,
                         5694,
                         8116,
                         11770,
                         12514,
                         15893,
                         20034,
                         17529,
                         17377,
                         15196,
                         27436,
                         21301,
                         12644,
                         13250,
                         17232,
                         28717,
                         17289,
                         11059,
                         14351,
                         14590,
                         20103,
                         10774,
                         15617,
                         19790,
                         17413]
                   }
)

@app.route('/get_facility')
def get_facility():

    return jsonify({'x':['샤워실 및 탈의실', '욕실', '음료대', '자동 판매기', '접수대 및 작업대', '세면대	', '장애인용 관람석', '점자블록', '객실 및 침실	',
       '경보 및 피난설비	', '자동 출입구(문)	', '장애인용 화장실', '장애인용 승강기', '장애인 전용 주차구역', '주출입구 높이차이 제거', '주출입구 접근로'],
                    'y' : [144,
                            144,
                            340,
                            340,
                            342,
                            396,
                            561,
                            597,
                            693,
                            807,
                            3192,
                            3204,
                            3742,
                            5971,
                            6631,
                            7034],

                    "x1": ['객실 및 침실',
 '경보 및 피난설비',
 '샤워실 및 탈의실',
 '세면대',
 '욕실',
 '음료대',
 '자동 출입구(문)',
 '자동 판매기',
 '장애인 전용 주차구역',
 '장애인용 관람석',
 '장애인용 승강기',
 '장애인용 화장실',
 '점자블록',
 '접수대 및 작업대',
 '주출입구 높이차이 제거',
 '주출입구 접근로'], "y1" : [693,
 807,
 144,
 396,
 144,
 340,
 3192,
 340,
 5971,
 561,
 3742,
 3204,
 597,
 342,
 6631,
 7034]
                    } )


@app.route('/eda')
def eda():
    places = Place.query.all()
    json_list = [i.serialize for i in places]
    json_list = json_list[:4000]
    return render_template('pages-contact.html', places=json_list)





if __name__ == '__main__':
    app.run()











