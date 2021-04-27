import os
import random
import time

from flask import current_app
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField, validators

from models import Question, db, QuestionTags, Answer


class WriteQuestionForm(FlaskForm):
    """ 写文章/问题 """
    img = FileField(label='题图', render_kw={
        'accept': '.jpeg, .jpg, .png'
    }, validators=[FileAllowed(['png', 'jpg', 'jpeg'], '请选择合适的图片类型')])
    title = StringField(label='标题', render_kw={
        'class': 'form-control',
        'placeholder': '请输入标题（最多50个字）'
    }, validators=[validators.DataRequired('标题必填'), validators.Length(min=2, max=50, message='标题长度为2-50字')])
    tags = StringField(label='标签', render_kw={
        'class': 'form-control',
        'placeholder': '输入标签，用空格分割'
    })
    desc = TextAreaField(label='简述', render_kw={
        'class': 'form-control',
        'placeholder': '简述'
    }, validators=[validators.Length(max=150, message='描述最长150字')])
    content = CKEditorField(label='内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入正文'
    }, validators=[validators.DataRequired('正文必填'), validators.Length(min=30, message='正文不能少于30个字')])

    def save(self):
        """ 发布问题 """
        # 1、获取图片
        img = self.img.data
        img_name = ''
        if img:
            img_name = '{}_{}_{}'.format(time.strftime('%Y_%m%d_%H%M%S', time.localtime()), random.randint(1000, 99999), secure_filename(img.filename))
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2、保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        que_obj = Question(title=title, desc=desc, img=img_name, content=content, user=current_user)
        db.session.add(que_obj)
        # 3、保存标签
        tags = self.tags.data
        for tag_name in tags.split(' '):
            if tag_name:
                tag_obj = QuestionTags(tag_name=tag_name, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return que_obj


class WriteAnswerForm(FlaskForm):
    """ 写回答 """
    content = CKEditorField(label='回答内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入正文'
    }, validators=[validators.DataRequired('回答内容不能为空'), validators.Length(min=9, message='评论不能少于9个字')])

    def save(self, question):
        """ 保存表单数据 """
        content = self.content.data
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
