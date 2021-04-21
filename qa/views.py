from flask import Blueprint, render_template

qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def index():
    """ 首页 """
    return render_template('index.html')


@qa.route('/follow')
def follow():
    """ 关注 """
    return render_template('follow.html')


@qa.route('/write')
def write():
    """ 写文章，提问 """
    return render_template('write.html')


@qa.route('/detail')
def detail():
    """ 问题详情 """
    return render_template('detail.html')
