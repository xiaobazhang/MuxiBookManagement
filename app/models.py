# coding: utf-8
"""
    models.py
    ~~~~~~~~~

        数据库文件
            保存用户的数据库文件,其中表结构如下
            数据库tables:
                                                        books

                 id                         Integer, primary_key                          主键
                 url                        String url                                    对应豆瓣API的get url
                 name                       String                                        书名
                 summary                    String(编码) resp['summary']返回值             概要，豆瓣API获取
                 image                      String(编码) resp['image']返回值 url           封面图，API获取
                 user_id                    Integer，ForeignKey 外键 与users表的id相关联    与借阅者关联
                 end                        String, 书籍到期时间
                 status                     Boolean, 书籍的借阅状态，如果为True则被借阅
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                        users

                 id                         Integer, primary_key                          主键
                 username                   String                                        用户名
                 password                   password_hash                                 密码散列值
                 user_type                  Integer                                       账户类型,学生,老师,管理员
                 use_time                   Integer                                       使用时间
                 use_flow                   Integer                                       使用流量(单位是M)
                 online_type                Integer                                       在线状态
"""
from . import db, login_manager, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sys


# python 3搜索的不兼容
if sys.version_info[0] == 3:
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy


class User(db.Model, UserMixin):
    """用户类"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(164))
    password_hash = db.Column(db.String(164))
    user_type = db.Column(db.Integer)
    use_time = db.Column(db.Integer)
    use_flow = db.Column(db.Integer)
    online_type = db.Column(db.Integer)

    @login_manager.user_loader
    def load_user(user_id):
        """flask-login要求实现的用户加载回调函数
           依据用户的unicode字符串的id加载用户"""
        return User.query.get(int(user_id))

    @property
    def password(self):
        """将密码方法设为User类的属性"""
        raise AttributeError('无法读取密码原始值!')

    @password.setter
    def password(self, password):
        """设置密码散列值"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码散列值"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "%r :The instance of class User" % self.username

# if enable_search:
#    whooshalchemy.whoosh_index(app, Book)
