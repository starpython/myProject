import hashlib
import random

from flask import Blueprint, render_template, request, g, session, redirect, url_for
from App.models import Article, db, Article_list, Admin

blue = Blueprint('blue', __name__)

#加密方法
def md5_password(password):
    m = hashlib.md5()
    m.update(password.encode())
    return  m.hexdigest()
    pass


@blue.route('/',methods=["GET","POST"])
def index():
    aa = Article()
    articlelist = aa.query.all()
    g.articlelist=articlelist
    bb = Article_list()
    articlelists = bb.query.all()
    g.articlelists=articlelists

    if request.method == 'POST':
        if request.form['keyboard']:
            search_data = request.form['keyboard']

            articlelists = Article_list.query.filter(Article_list.title.contains(search_data))
            if not articlelists:
                return 'nothing find'
        else:
            # 404收入为空
            return render_template('nothingGetForSearch.html')
    return render_template('index.html',articlelist = articlelist, articlelists = articlelists)

@blue.route('/<data>/')
def check(data):
    p=Article()
    articlelist = p.query.all()
    bb = Article_list()
    articlelists = bb.query.all()
    data = Article.query.filter_by(block_article=data).first()
    if data:
        articlelists = data.article

    return render_template('index.html', articlelist=articlelist, articlelists=articlelists)

@blue.route('/search/',methods=["GET","POST"])
def search():
    p=Article()
    data = p.query.all()
    print(data)
    return "ok"


@blue.route('/admin/')
def admin_login():
    return render_template('admin_login.html')

@blue.route('/admin_index/',methods=["GET","POST"])
def admin_index():
    if request.method == "POST":
        username = request.form.get('username')
        userpassword = md5_password(request.form.get('userpwd'))

        person = Admin.query.filter_by(name=username,password=userpassword)
        if not person:

            #考虑密码错误后加入验证码

            return render_template('admin_login.html')
        session['username'] = username
        #要使用session加密和md5加密和用戶名登錄有效时间
        session['password'] = userpassword
        return render_template('admin_index.html',username = username)
    else:
        tempdata=session.get('username','')
        if not tempdata:
            return render_template('admin_login.html')
        return render_template('admin_index.html',username = tempdata)

@blue.route('/admin_index/article',methods=["GET","POST"])
def article():
    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')

    articlelists = Article_list.query.all()
    return render_template('article.html',articlelists=articlelists)

@blue.route('/admin_index/article_add',methods=["GET","POST"])
def article_add():
    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')
    if request.method == "POST" :
        newArticle = Article_list()
        newArticle.title = request.form.get('title')
        newArticle.content = request.form.get('content')[3:-3]
        newArticle.type = request.form.get('category')
        newArticle.pic = random.randint(1,11)
        try:
            db.session.add(newArticle)
            db.session.commit()
            return "done"
        except:
            db.session.rollback()
            db.session.flush()
            return  "error"
        articlelists = Article_list.query.all()
        return render_template('article.html', articlelists=articlelists)
    p = Article()
    articlelist = p.query.all()
    return render_template('add-article.html',articlelist = articlelist)


@blue.route('/admin_index/article_update/<titlename>/',methods=["GET","POST"])
def article_update(titlename):
    #titlename更新文章的名称，作为标志
    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')
    #更改的文章
    if request.method == "POST" :
        updateArticle =Article_list.query.filter_by(title = request.form.get("title","")).first()
        #判断内容是否有更改not
        updateArticle.title = request.form.get('title')
        updateArticle.content = request.form.get('content')
        updateArticle.type = request.form.get('type')

        try:
            db.session.commit()
            return "done"
        except:
            db.session.rollback()
            db.session.flush()
            return  "error"
        articlelists = Article_list.query.all()
        return render_template('article.html', articlelists=articlelists)

    #显示更改条目
    articlelists = Article_list.query.filter_by(title=titlename)
    p = Article()
    articlelist = p.query.all()
    #保存checked标签
    data=[]
    #print(type(articlelists.first()),articlelists.first(),articlelists.first().title)
    for i in articlelist:
        #print(i.block_article,articlelists.first().type)
        if i.block_article == articlelists.first().type :
            data.append({"title":i.block_article,'mark':"checked"})
        else:
            data.append({"title":i.block_article,'mark':""})
    print(articlelists.first().title)
    return render_template('update-article.html',articlelist = data,articlelists=articlelists.first())

@blue.route('/admin_index/article_del/',methods=["GET","POST"])
def article_del():
    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')
    if request.method == "POST" :

        values1 = list(request.form.to_dict().values())
        for del_art in values1:
            del_article = Article_list.query.filter_by(title=del_art)
            try:
                db.session.delete(del_article)
                db.session.commit()
                return "done"
            except:
                db.session.rollback()
                db.session.flush()
                return  "error"

    return redirect(url_for('blue.article'))

@blue.route('/admin_index/category/',methods=["POST","GET"])
def category():
    tempdata = session.get('username', '')
    if not tempdata:
        return render_template('admin_login.html')
    if request.method == "POST":
        return "change"
    #栏目总数，数目顺序,单个所拥有的article数目,别名
    data_category = []
    mark_category = 0
    articlelist = Article.query.all()
    for detail in articlelist:
        mark_category += 1
        count = Article_list.query.filter(Article_list.type == detail.block_article).count()
        data_category.append({"id":mark_category,"name":detail.block_article,"count":count,"smallname":"无"})

    return render_template('category.html',articlelist=data_category,mark_category = mark_category)


@blue.route('/admin_index/category_add',methods=["GET","POST"])
def category_add():

    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')
    if request.method == "POST" :
        newCategory = Article()
        newCategory.block_article = request.form.get("name")
        try:
            db.session.add(newCategory)
            db.session.commit()

        except:
            db.session.rollback()
            db.session.flush()
            return  "error"

    return redirect('url_for(blue.category)')


@blue.route('/admin_index/category_update/<titlename>/',methods=["GET","POST"])
def category_update(titlename):
    #titlename更新文章的名称，作为标志
    tempdata=session.get('username','')
    if not tempdata:
        return render_template('admin_login.html')
    #更改的文章

    if request.method == "POST" :

        updateCategory =Article_list.query.filter_by(block_article = titlename).first()
        #判断内容是否有更改not
        updateCategory.block_article = request.form.get('name')

        try:
            db.session.commit()

        except:
            db.session.rollback()
            db.session.flush()
            return  "error"

        return redirect('url_for(blue.category)')

    #显示更改条目
    articlelist = Article.query.filter_by(block_article=titlename).first()
    data = Article.query.all()
    return render_template('update-category.html',articlelist = articlelist,data = data)


@blue.route('/admin_index/category_del/<titlename>/')
def category_del(titlename):
    tempdata=session.get('username','')

    if not tempdata:
        return render_template('admin_login.html')



    del_article = Article.query.filter_by(title=titlename)
    try:
        db.session.delete(del_article)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()
        return  "error"

    return redirect(url_for('blue.category'))


@blue.route('/get/')
def get():
    p=Article()
    data = p.query.all()
    print(data)
    return "ok"

