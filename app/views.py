# coding: utf-8

from . import app, db
from werkzeug.utils import secure_filename
from functools import wraps
from app.models import User
from app.forms import BookForm, GetForm, LoginForm, RterForm
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from urllib2 import urlopen
import json
import datetime
import os

# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    """检查文件扩展名函数"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 对所有访客可见
@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('base.html')


# 对所有访客可见
@app.route('/search', methods=["POST", "GET"])
def search():
    """
    搜索视图函数

        1. 搜索表单
        2. 显示搜索结果列表(最多加载5条搜索结果)

        搜索模式：
            1. 书名搜索（书名必须正确）
            2. 类别搜索（返回类别的图书：后台、前端、设计、互联网、其他）
    """
    if request.methos == 'POST':
        """前端 input 标签 action 实现重定向
           递交 search_results 处理"""
        pass


# 对所有访客可见
@app.route('/search_results/', methods=["POST", "GET"])
def search_results():
    """
    搜索结果页

        提供书籍借阅表单
    """
    form2 = LoginForm()
    get_book_list = []
    search = request.args.get('search')
    results = Book.query.whoosh_search(search, app.config['MAX_SEARCH_RESULTS'])

    for book in results[:]:
        """
        # 默认搜索结果全部为可借阅图书
        if request.args.get('range') == 'can':
            if book.status != True:
            # 跳过不可借阅图书
                get_book_list.append(book)
        if request.args.get('range') == 'all':
            get_book_list.append(book)
        """
        get_book_list.append(book)

    return render_template('search_results.html',
                           get_book_list=get_book_list,
                           search=search,
                           form2=form2)


# 对所有访客可见，但只有登录用户可以借阅(html改动)
@app.route('/info/<name>', methods=["POST", "GET"])
def info(name):
    form = GetForm()
    form2 = LoginForm()
    book = Book.query.filter_by(name=name).first()
    if form.validate_on_submit():
        day = form.day.data
        if int(day) >= 0:
            start = datetime.datetime.now()
            book.start = start
            book.user_id = current_user.id
            book.status = True  # 已被借
            book.end = (start + datetime.timedelta(day)).strftime("%Y-%m-%d %H:%M:%S")
            return redirect(url_for('user', id=current_user.id))
        else:
            flash('光阴似箭、岁月如梭,时间－你不能篡改她，更不能逆转她!')
    return render_template('info.html', book=book, form=form,  form2=form2)


@app.route('/login', methods=["POST", "GET"])
def login():
    """用户登录接口

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('user', id=current_user.id))
        flash('用户名或密码错误!')
"""
    return render_template('new_login.html')



# 只对管理员可见
@app.route('/rter', methods=["POST", "GET"])
@login_required
def rter():
    """用户注册接口"""
    if current_user.username == 'neo1218':
        form = RterForm()
        if form.validate_on_submit():
            u = User(username=form.username.data, password=form.password.data)
            db.session.add(u)
            db.session.commit()
        return render_template('r.html', form=form)
    else:
        return redirect(url_for('home'))


# 只对管理员可见
@app.route('/bookin', methods=["POST", "GET"])
@login_required
def bookin():
    """
    书籍录入

        输入书籍的名字，将书籍的

            书名， 封面， 简介 录入数据库
    """
    if current_user.username == 'neo1218':
        form = BookForm()

        if form.validate_on_submit():
            bookname = form.bookname.data
            get_url = "https://api.douban.com/v2/book/search?q=%s" % bookname
            resp_1 = json.loads(urlopen(get_url).read().decode('utf-8'))
            book_id = resp_1['books'][0]['id']
            url = "https://api.douban.com/v2/book/%s" % book_id
            resp_2 = json.loads(urlopen(url).read().decode('utf-8'))
            book = Book(url=url, name=resp_2['title'], author=resp_2['author'][0], \
                        tag=form.tag.data, summary=resp_2['summary'], \
                        image=resp_2['images'].get('large'), user_id=None, end=None, \
                        status=False)
            db.session.add(book)
            db.session.commit()
            flash('书籍已录入！')
            return redirect(url_for('bookin'))
        return render_template('bookin.html', form=form)
    else:
        return redirect(url_for('home'))


# 对所有登录用户可见
@app.route('/logout')
@login_required
def logout():
    """退出视图函数"""
    logout_user()
    return redirect(url_for('home'))


# 对登录用户可见
@app.route('/user/<int:id>', methods=["POST", "GET"])
def user(id):
    """
    用户个人信息页
        显示该用户历史借阅
        显示该用户快要过期的书（3天为界）

        提供用户还书按钮

        借阅图书默认按归还时间顺序排序
    """
    book_list = Book.query.filter_by(user_id=current_user.id).order_by('end').all()
    time_done_book = []
    time_dead_book = []

    for book in book_list:
        delta = (datetime.datetime.strptime(book.end, "%Y-%m-%d %H:%M:%S") - \
            datetime.datetime.now()).total_seconds()
        if delta <= 3*24*60*60 and delta > 0:
            time_done_book.append(book)
        if delta <= 0:
            time_dead_book.append(book)

    if request.method == "POST":
        """在前端input标签的重定向页面进行处理"""
        return redirect(url_for('user', id=current_user.id))

    books = Book.query.filter_by(name=request.args.get('back'), user_id=current_user.id).all()
    for book in books:
        book.status = False
        book.start = None
        book.end = None
        book.user_id = None
        flash('%s 已归还!' % book.name)
        return redirect(url_for('user', id=current_user.id))

    range_book_count = range(len(book_list)/3 + 1)
    range_timedonebook_count = range(len(time_done_book)/3 + 1)

    return render_template('user.html',
                           time_done_book=time_done_book[:2],
                           book_list=book_list,
                           range_book_count=range_book_count,
                           range_timedonebook_count=range_timedonebook_count,
                           session=session)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload_file():
    """上传文件函数"""
    session['fileurl'] = 'http://127.0.0.1:5000/static/image/logo.png'
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['fileurl'] = 'http://121.0.0.1:5000/static/image/%s' % filename
            return redirect(url_for('user', username=current_user.username))
    return render_template('upload.html')
