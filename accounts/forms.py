import hashlib

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Length, ValidationError

from models import User, db, UserProfile
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """ 用户注册 """
    username = StringField(label='用户名：', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[validators.DataRequired('请输入用户名'), phone_required])
    nickname = StringField(label='昵称：', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入昵称'
    }, validators=[validators.DataRequired('请输入昵称'), Length(min=2, max=20, message='昵称长度在2-20之间')])
    password = PasswordField(label='密码：', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[validators.DataRequired('请输入密码')])
    re_password = PasswordField(label='确认密码：', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请再次输入密码'
    }, validators=[validators.DataRequired('请输入确认密码'), validators.EqualTo('re_password', message='两次密码输入不一致')])

    def validate_username(self, field):
        """ 检测用户名是否已经存在 """
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户已经存在')
        return field

    def register(self):
        """ 自定义的用户注册函数 """
        # 1、获取表单信息
        username = self.username.data
        nickname = self.nickname.data
        password = self.password.data
        # 2、添加到db.session
        try:
            # 将密码加密存储
            password = hashlib.md5(password.encode()).hexdigest()
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, nickname=nickname, password=password)
            db.session.add(user_obj)
            profile_obj = UserProfile(username=username, user=user_obj)
            db.session.add(profile_obj)
            db.session.commit()
            return user_obj
        except Exception as e:
            print(e)
        return None