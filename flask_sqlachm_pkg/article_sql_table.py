#coding: utf8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

global db
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(100), nullable= False)

    def __init__(self):
        pass

article_tag = db.Table('article_tag', db.metadata,
       db.Column('article_id', db.Integer, db.ForeignKey('article.id'), nullable=False, primary_key= True),
       db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key= True))

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    # author = db.Column(db.String(50), db.ForeignKey('author.author' , name=))
    time = db.Column(db.DateTime, default=datetime.now())
    content = db.Column(db.Text, nullable=False)

    # 和author的关系，一对多
    authorid = db.Column(db.Integer, db.ForeignKey('author.id'))
    ref = db.relationship('Author', backref='bref')

    # 和tag的关系，多对多
    tags = db.relationship('Tag', secondary = article_tag)

    def __repr__(self):
        return '<User(id="%s",title="%s",author="%s",content="%s,time=%s")>'%(self.id,self.author,self.title, self.content,self.time)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable= False)

    # 和article的关系，多对多
    articles = db.relationship('Article',secondary = article_tag)

def installapp(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Chiloon@localhost:3306/a?charset=utf8'
    global db
    db.init_app(app)
    db.create_all()




