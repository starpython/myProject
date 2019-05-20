from App.exts import db


# 模型 => 类
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    block_article = db.Column(db.String(50), unique=True)
    article = db.relationship('Article_list',backref='getArticle',lazy=True)

class Article_list(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True)
    content = db.Column(db.String(150))
    pic = db.Column(db.String(5))
    type = db.Column(db.String(20),db.ForeignKey(Article.block_article))

class Admin(db.Model):
    id = db.Column( db.INTEGER ,primary_key=True,autoincrement=True)
    name = db.Column( db.String(30),unique=True)
    password = db.Column( db.String(50))

