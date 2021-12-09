from flask import Flask, session, g
from flask_ckeditor import CKEditor
from flask_login import LoginManager

from models import db, User
from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split, dt_format_show

app = Flask(__name__, static_folder='medias')
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# 富文本初始化
ckeditor = CKEditor()
ckeditor.init_app(app)

# 登录验证flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'
login_manager.login_message = '请您登录后再操作！'
login_manager.login_message_category = 'info'

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split
app.jinja_env.filters['dt_format_show'] = dt_format_show


# flask-login登录
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
