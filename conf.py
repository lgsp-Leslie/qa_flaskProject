import os


class Config(object):
    """ 项目的配置文件 """
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_qa'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = '9595'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
    # 分页，每页数据的大小
    PER_PAGE = 2
