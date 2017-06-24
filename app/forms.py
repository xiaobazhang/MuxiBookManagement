# coding: utf-8

"""
    forms.py
    ~~~~~~~~

        登录后台表单
"""
from flask_wtf import Form
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class SearchForm(Form):
    """搜索表单🔍"""
    search = StringField('完整书名or类别名', validators=[DataRequired()])
    status1 = BooleanField('可借')
    status2 = BooleanField('全部')
    submit = SubmitField('搜索')


class BookForm(Form):
    """录入表单"""
    bookname = StringField('书名', validators=[DataRequired()])
    tag = StringField('类别(后台、设计、前端、互联网、其他)', validators=[DataRequired()])
    submit = SubmitField('录入')


class LoginForm(Form):
    """登录表单"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('login')


class GetForm(Form):
    """借阅表单"""
    status = BooleanField('借阅')
    day = IntegerField('借阅天数')
    submit = SubmitField('确定借阅')


class BackForm(Form):
    """归还表单"""
    status = BooleanField('归还')
    back = SubmitField('归还此书')


class RterForm(Form):
    """注册表单"""
    username = StringField('用户名')
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password1', message="密码匹配")])
    password1 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')
