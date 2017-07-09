# coding: utf-8

"""
    forms.py
    ~~~~~~~~

        登录后台表单
"""
from flask_wtf import Form
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(Form):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(message=u'邮箱不能为空')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码', default=False)
    submit = SubmitField('登录')

class RterForm(Form):
    """注册表单"""
    username = StringField('用户名', validators=[DataRequired()])
    user_email = StringField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password1', message="密码必须一致")])
    password1 = PasswordField('确认密码', validators=[DataRequired()])
    verification_code = StringField(u'验证码', validators=[DataRequired(), Length(4, 4, message=u'填写4位验证码')])
    submit = SubmitField('注册')
