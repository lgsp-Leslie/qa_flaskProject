from flask import Blueprint, render_template, redirect, flash, url_for, session, request

from accounts.forms import RegisterForm, LoginForm
from models import User, UserLoginHistory, db

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录页面 """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 1、查找对应的用户
        user = User.query.filter_by(username=username, password=password).first()
        # 2、登录用户
        session['user_id'] = user.id
        # 3、记录日志
        ip = request.remote_addr
        ua = request.headers.get('user-agent', None)
        obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
        db.session.add(obj)
        db.session.commit()
        # 4、跳转到首页
        flash('{}，欢迎登录在线问答系统！'.format(user.nickname), 'success')
        return redirect(url_for('qa.index'))
    else:
        pass
    return render_template('login.html', form=form)


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册 """
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            # 3、跳转到成功页面
            flash('注册成功，请登录！', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('注册失败，请稍后再试。', 'danger')
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')

