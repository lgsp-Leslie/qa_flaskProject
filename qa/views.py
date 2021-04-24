from flask import Blueprint, render_template, request, abort
from flask_login import login_required

from conf import Config
from models import Question

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
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('follow.html', page_data=page_data)


@qa.route('/write')
@login_required
def write():
    """ 写文章，提问 """
    return render_template('write.html')


@qa.route('/detail/<int:q_id>')
def detail(q_id):
    """ 问题详情 """
    # 1、查询问题信息
    question = Question.query.get(q_id)
    if not question.is_valid:
        abort(404)
    # 2、展示第一条回答信息
    answer = question.answer_list.filter_by(is_valid=True).first()
    return render_template('detail.html', question=question, answer=answer)
