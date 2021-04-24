from flask import Blueprint, render_template, redirect, flash, url_for, session, request, g
from flask_login import login_user, logout_user, login_required

from accounts.forms import RegisterForm, LoginForm
from models import User, UserLoginHistory, db

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录页面 """
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    print(next_url)
    if form.validate_on_submit():
        user = form.do_login()
        if user:
            # 4、跳转到指定页面或首页
            flash('{}，欢迎登录在线问答系统！'.format(user.nickname), 'success')
            return redirect(next_url)
        else:
            flash('登录失败，请稍后重试', 'danger')
    # else:
    #     print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout')
def logout():
    """ 退出登录 """
    # 自定义登录的退出
    # session['user_id'] = ''
    # g.current_user = None
    # flask-login登录的退出
    logout_user()
    flash('期待下一次相见！', 'success')
    return redirect(url_for('accounts.login'))


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
@login_required
def mine():
    """ 个人中心 """
    return render_template('mine.html')

