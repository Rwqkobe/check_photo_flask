from flask_wtf import FlaskForm
from wtforms import RadioField,SubmitField
from wtforms.validators import DataRequired


class DataForm(FlaskForm):
    weather = RadioField('天气类型：',
                         choices=[('normal', '正常'), ('rain', '雨天'), ('snow', '雪天'), ('fog', '雾天'),('others','其他')],
                         validators=[DataRequired],default='normal')
    road = RadioField('道路类型：',
                         choices=[('urban', '城市'), ('highway', '高速'), ('country', '郊区'), ('tunnel', '隧道'),('others','其他')],
                         validators=[DataRequired],default='urban')
    time = RadioField('时间段：',
                         choices=[('day', '白天'), ('night', '夜晚'),('others','其他')],
                         validators=[DataRequired],default='day')
    next_pic = SubmitField('下一张')
    foreign_pic = SubmitField('上一张')