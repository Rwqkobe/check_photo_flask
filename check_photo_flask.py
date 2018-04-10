from flask import Flask, render_template, request, flash, redirect, url_for
from utils import *
from DateForm import DataForm
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/hobot_data_test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rwq'
db = SQLAlchemy(app)

g = None
g_img_url = None
temp_list = list()


# 还差远程登录
# img_url = r"static/baidu.png"
@app.route('/', methods=['GET', ])
def index_0():
    global g
    global g_img_url
    global temp_list
    print('index_0,img_url =', g_img_url, datetime.datetime.now())
    try:
        if temp_list == []:
            g_img_url = next(g)
        else:
            g_img_url = temp_list.pop()
    except StopIteration:
        g_img_url = '已完成'
    return redirect(url_for('index', img_url=g_img_url))


@app.route('/<img_url>', methods=['GET', 'POST'])
def index(img_url):
    global g
    global g_img_url
    data_form = DataForm()
    if request.method == 'GET':
        if img_url == '已完成':
            return '已完成'
        else:
            try:
                l = img_url.split('\\')
                relative_url = l[-3] + '\\' + l[-2] + '\\' + l[-1]
            except:
                relative_url = ''  # 奇怪的错误
            return render_template('index.html', relative_url=relative_url, img_url=img_url, form=data_form)
    elif request.method == 'POST':
        print('go in to post')
        weather = request.form.get('weather')
        road = request.form.get('road')
        time = request.form.get('time')
        try:
            try:
                # save_to_db(img_url, weather=weather, road=road, daynight=time)
                save_to_mysql(img_url=img_url, weather=weather, road=road, daynight=time)
                db.session.commit()
                print('save success ',img_url)
            except:
                print('save to db error')
            img_url = next(g)
            g_img_url = img_url
        except StopIteration:
            img_url = '已完成'
            g_img_url = img_url
        return redirect(url_for('index', img_url=img_url))

    else:
        flash('请求方式有误！')

def save_to_mysql(img_url, weather, road, daynight):
    data_id = parse_data_id(img_url)
    year, time, hour = parse_year_time_hour(img_url)
    key = data_id + "_" + year + "_" + str(int(hour))
    Weather.query.filter_by(key=key).update({'weather': weather, 'road': road, 'daynight': daynight})


class DataModel(db.Model):
    __tablename__ = 'image_data'
    data_type = db.Column(db.String(20))  # data_type = train or test
    type = db.Column(db.String(20))  # type = vehicle or pedestrian or dms ...
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_id = db.Column(db.String(20))
    version = db.Column(db.Integer)

    key = db.Column(db.String(100), unique=True)
    image_key = db.Column(db.String(100))
    video_name = db.Column(db.String(100))
    video_index = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    # time
    year = db.Column(db.String(20))
    hour = db.Column(db.Integer)
    time = db.Column(db.String(20))
    # calculate
    rect_num = db.Column(db.Integer)
    # fill by us
    weather = db.Column(db.String(20))
    road = db.Column(db.String(20))
    daynight = db.Column(db.String(20))

    # db.relationships
    # lane = db.relationship()  # 车道线
    # vehicle = db.relationship('Vehicle', backref=db.backref('body'))  # vehicle中的属性
    # person = db.relationship('Person', backref=db.backref('body'))
    # head = db.relationship('Head', backref=db.backref('body'))
    # traffic_sign = db.relationship('Traffic_sign', backref=db.backref('body'))
    # hand = db.relationship()
    # face_keypoint_8 = db.relationship()
    # face_keypoint_72 = db.relationship()
    # shoulder_foot_keypoint_4 = db.relationship()
    # plate_box = db.relationship()
    # plate_point = db.relationship()
    # parsing = db.relationship()
    # recognition = db.relationship()
    # voice = db.relationship()
    # classify = db.relationship()
    # belong_to = db.relationship()


# class Person(db.Model):
#     __tablename__ = 'person'
#     # identity
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     key = db.Column(db.String(100), db.ForeignKey('image_data.key'))
#     # rect
#     height = db.Column(db.Float(precision=1))
#     width = db.Column(db.Float(precision=1))
#     area = db.Column(db.Integer)
#     diagonal = db.Column(db.Float(precision=1))
#     h_div_w = db.Column(db.Float(precision=1))
#     # attrs
#     pose = db.Column(db.String(20))
#     type = db.Column(db.String(20))
#     # others
#     ignore = db.Column(db.String(20))
#     blur = db.Column(db.String(20))
#     occlusion = db.Column(db.String(20))
#     hard = db.Column(db.String(20))
#
#
# class Head(db.Model):
#     __tablename__ = 'head'
#     # identity
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     key = db.Column(db.String(100), db.ForeignKey('image_data.key'))
#     # rect
#     height = db.Column(db.Float(precision=1))
#     width = db.Column(db.Float(precision=1))
#     area = db.Column(db.Integer)
#     diagonal = db.Column(db.Float(precision=1))
#     h_div_w = db.Column(db.Float(precision=1))
#     # attrs
#     gender = db.Column(db.String(20))
#     has_glasses = db.Column(db.String(20))
#     hair = db.Column(db.String(20))
#     age = db.Column(db.String(20))
#     new_age = db.Column(db.String(20))
#     has_hat = db.Column(db.String(20))
#     look = db.Column(db.String(20))
#     # others
#     left_eye = db.Column(db.String(20))
#     right_eye = db.Column(db.String(20))
#     orientation = db.Column(db.String(20))
#     occlusion = db.Column(db.String(20))
#     ignore = db.Column(db.String(20))
#     hard = db.Column(db.String(20))
#
#
# class Vehicle(db.Model):
#     __tablename__ = 'vehicle'
#     # identity
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     key = db.Column(db.String(100), db.ForeignKey('image_data.key'))
#     # rect
#     height = db.Column(db.Float(precision=1))
#     width = db.Column(db.Float(precision=1))
#     area = db.Column(db.Integer)
#     diagonal = db.Column(db.Float(precision=1))
#     h_div_w = db.Column(db.Float(precision=1))
#     # attrs
#     type = db.Column(db.String(30))
#     part = db.Column(db.String(30))
#     color = db.Column(db.String(30))
#     light = db.Column(db.String(20))
#     # others
#     score = db.Column(db.Float(precision=1))
#     ignore = db.Column(db.String(20))
#     blur = db.Column(db.String(20))
#     occlusion = db.Column(db.String(20))
#     hard_sample = db.Column(db.String(20))
#
#
# # 交通标志牌
# class Traffic_sign(db.Model):
#     __tablename__ = 'traffic_sign'
#     # identity
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     key = db.Column(db.String(100), db.ForeignKey('image_data.key'))
#     # rect
#     height = db.Column(db.Float(precision=1))
#     width = db.Column(db.Float(precision=1))
#     area = db.Column(db.Integer)
#     diagonal = db.Column(db.Float(precision=1))
#     h_div_w = db.Column(db.Float(precision=1))
#     # attrs
#     type = db.Column(db.String(30))
#     value = db.Column(db.String(30))
#     # others
#     ignore = db.Column(db.String(20))
#     occlusion = db.Column(db.String(20))
#     hard = db.Column(db.String(20))


class Weather(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(100), db.ForeignKey('image_data.key'))
    weather = db.Column(db.String(20))
    road = db.Column(db.String(20))
    daynight = db.Column(db.String(20))


i = 1


def fill_used_list():
    global i
    used_key_list = list()
    for row in Weather.query.all():
        if row.road=="" or row.road is None:
            print('not none', i)
            i += 1
        else:
            used_key_list.append(row.key)


        # if row.road != '':
        #     used_key_list.append(row.key)
        # else:
        #     print('not none', i)
        #     i += 1
    return used_key_list


if __name__ == '__main__':
    g = grab_img_url()  # g : Iterator
    app.run(host='0.0.0.0')

# ip : 10.64.34.95:5000
# wlan ip : 10.64.37.72:5000