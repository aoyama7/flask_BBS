from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, InputRequired)


class RegisterForm(FlaskForm):
    # 注册表单类
    email = StringField(validators=[DataRequired('邮箱不能为空'), Email('请输入正确的邮箱格式')])
    username = StringField(validators=[DataRequired('用户名不能为空'), Length(6, 20, '密码长度为 6 ~ 20 个字符')])
    repeat_password = PasswordField(validators=[EqualTo('password', '两次输入的密码不一致')])
    vercode = StringField(validators=[InputRequired('答案错误')])


class LoginForm(FlaskForm):
    # 登录表单类
    email = StringField(validators=[DataRequired('邮箱不能为空')])
    password = PasswordField(validators=[DataRequired('密码不能为空'), Length(3, 26, '密码长度为 3 ~ 26 个字符')])
    vercode = StringField(validators=[InputRequired('答案错误')])