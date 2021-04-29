from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from conf import Config
from models import Question, Answer, AnswerComment, db
from qa.forms import WriteQuestionForm, WriteAnswerForm

qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def index():
    """ 首页 回答列表 """
    page = int(request.args.get('page', 1))
    page_data = Answer.query.filter_by(is_valid=True).order_by(Answer.updated_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)

    return render_template('index.html', page_data=page_data)


@qa.route('/follow_page')
def follow_page():
    """ 关注 问题列表 """
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).order_by(Question.updated_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('follow_page.html', page_data=page_data)


@qa.route('/follow')
def follow():
    """ 关注 """
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).order_by(Question.updated_at.desc()).paginate(page=page,
                                                                                                      per_page=Config.PER_PAGE)
    return render_template('follow.html', page_data=page_data)


@qa.route('/qa/list')
def question_list():
    """ 查询问题数据列表 """
    """
    json
    {
        'code': 0,
        'data': '',
    }
    """
    try:
        page = int(request.args.get('page', 1))
        page_data = Question.query.filter_by(is_valid=True).order_by(Question.updated_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
        data = render_template('qa_list.html', page_data=page_data)
        code = 0
    except Exception as e:
        print(e)
        data = ''
        code = 1
    return {'code': code, 'data': data}


@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """ 写文章，提问 """
    form = WriteQuestionForm()
    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('问题发布成功', 'success')
                return redirect(url_for('qa.detail', q_id=que_obj.id))
        except Exception as e:
            print(e)
            flash('问题发布失败，请稍后重试', 'danger')
    return render_template('write.html', form=form)


@qa.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):
    """ 问题详情 """
    # 1、查询问题信息
    question = Question.query.get(q_id)
    if not question.is_valid:
        abort(404)
    # 2、展示第一条回答信息
    answer = question.answer_list.filter_by(is_valid=True).first()

    # 添加回答
    form = WriteAnswerForm()
    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                flash('您尚未登录,请先登录！', 'danger')
                return redirect(url_for('accounts.login'))
            answer_obj = form.save(question=question)
            print(answer_obj)
            if answer_obj:
                flash('回答问题成功', 'success')
                return redirect(url_for('qa.detail', q_id=q_id))
        except Exception as e:
            print(e)
            print(form.errors)
            flash('回答问题失败，稍候再试', 'danger')

    return render_template('detail.html', question=question, answer=answer, form=form)


@qa.route('/comments/<int:answer_id>', methods=['GET', 'POST'])
def comments(answer_id):
    """ 评论 """
    answer = Answer.query.get(answer_id)
    if request.method == 'POST':
        # 添加评论，保存到数据库
        try:
            if not current_user.is_authenticated:
                result = {'code': 1, 'message': '请登录'}
                return jsonify(result), 400
            # 获取数据
            content = request.form.get('content', '')
            reply_id = request.form.get('reply_id', None)
            question = answer.question
            comment_obj = AnswerComment(content=content, user=current_user, answer=answer, reply_id=reply_id, question=question)
            db.session.add(comment_obj)
            db.session.commit()
            result = {'code': 0, 'message': '评论成功'}
            return jsonify(result), 201
        except Exception as e:
            result = {'code': 2, 'message': '服务器正忙，请稍后重试'}
            return jsonify(result), 500
    else:
        # 获取评论
        pass

