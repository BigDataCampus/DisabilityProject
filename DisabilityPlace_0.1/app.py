from flask import Flask, render_template, request, jsonify, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask import session, escape

import json


app = Flask(__name__)
app.config.update({'SECRET_KEY':'password'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB3.db'
db = SQLAlchemy(app)


# For more configuration options, check out the documentation
@app.route('/a')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



admin = Admin(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Place(db.Model):
    __tablename__ = 'Place'
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
    place_ID = db.Column(db.Integer,db.ForeignKey("Place.place_ID"))

    @property
    def serialize(self):
        return {
            'facility_ID':self.facility_ID,
            'facility_available_name':self.facility_available_name,
            'facility_is_available':self.facility_is_available,
            'place_ID':self.place_ID
        }

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Place, db.session))
admin.add_view(ModelView(Facility, db.session))


@app.route('/', methods=['POST', 'GET'])
def place_Setting():
    content = request.args.get("content")
    print("ccc:",content)

    if request.method == 'GET':
        if content:
            places = Place.query.filter(Place.place_name.like('%' + content + '%'))
        else:
            places = Place.query.all()
    else :
        pass
        # lat = request.form['lat']
        # lng = request.form['lng']
        # print(lat, lng)
        # from CF import contentCF
        # cf = list(contentCF(lat, lng))
        # cf = map(int, cf)
        # places = Place.query.filter(Place.place_ID.in_(cf)).all()

    json_list = [i.serialize for i in places]
    faclist = ['객실 및 침실',
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
'주출입구 접근로',]
    return render_template('base2.html', places = json_list, faclist = faclist)


@app.route('/getData')
def getData():
    data = request.args.get('a')
    print("getdata place_id : ", data)
    places = Place.query.filter_by(place_ID=data)
    fac = Facility.query.filter_by(place_ID=data)

    p = [i.serialize for i in places]
    f = [i.serialize for i in fac]
    return jsonify(json.dumps(p), json.dumps(f))


@app.route('/listings-single/<place_id>')
def place_SingleListing(place_id):
    info = Place.query.filter_by(place_ID=place_id)
    facinfo = Facility.query.filter_by(place_ID = place_id)

    return render_template("listings-single-page.html", info = info.all(), facinfo = facinfo.all())

@app.route('/getCF', methods=['POST'])
def getCF():
    lat = request.form['lat']
    lng = request.form['lng']
    selectedfac = request.form['selectedfac']
    print(selectedfac, type(selectedfac))
    print(lat, lng)
    cf = list(contentCF(selectedfac, lat, lng))
    cf = list(map(int, cf))
    print(cf)
    places = Place.query.filter(Place.place_ID.in_(cf)).all()
    p = [i.serialize for i in places]
    print("places result serialize : ", p)
    return json.dumps(p)


import pandas as pd
from sklearn.neighbors import NearestNeighbors

def contentCF(selectedfac, lat, lng):
    places = Place.query
    facility = Facility.query

    dfplaces = pd.read_sql(places.statement, places.session.bind)
    dffac = pd.read_sql(facility.statement, facility.session.bind)

    dummy = pd.get_dummies(dffac, columns=['facility_available_name']).groupby(['place_ID'], as_index=False).sum()
    dummy = dummy.merge(dfplaces)

    print(dummy.info())
    dummy.drop('place_name', axis=1, inplace=True)
    dummy.drop('facility_ID', axis=1, inplace=True)
    dummy.drop(['category', 'place_address'], inplace=True, axis=1)

    dummy.columns = ['place_id','객실 및 침실',
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
'주출입구 접근로','lat', 'lng']

    X = dummy.iloc[:, 1:]
    print(X.head())
    nbrs = NearestNeighbors(n_neighbors=5).fit(X)

    t = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, lat, lng]

    s = selectedfac.split(',')
    print(s)
    for i in s:
        t[int(i)-1] += 1

    print("knn t ",t,"\n result :",nbrs.kneighbors([t]))

    return nbrs.kneighbors([t])[1][0]


# eda -->
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


@app.route('/eda1')
def eda1():
    places = Place.query.all()
    json_list = [i.serialize for i in places]
    json_list = json_list[:4000]
    return render_template('dashboard-totalfacility.html', places=json_list)

@app.route('/eda2')
def eda2():
    return render_template('dashboard-facility-eda-map.html')

@app.route('/eda3')
def eda3():
    return render_template('dashboard-after-facility-map.html')

# eda-->

if __name__ == '__main__':
    app.run()











