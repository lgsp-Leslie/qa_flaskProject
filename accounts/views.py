from flask import Blueprint, render_template

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login')
def login():
    """ 登录页面 """
    return render_template('login.html')


@accounts.route('/register')
def register():
    """ 注册 """
    return render_template('register.html')


@accounts.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')

