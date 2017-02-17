#coding:utf8
from flask import Flask,render_template,views,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import flask

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Chiloon@localhost:3306/a?charset=utf8'
db = SQLAlchemy(app)

def post_article_info():
    article = {}
    article['title'] = flask.request.form.get('title')
    article['author'] = flask.request.form.get('author')
    article['content'] = flask.request.form.get('content')
    article['tag'] = flask.request.form.getlist('tag')
    return article


class Pubview(views.MethodView):
    def get(self):
        return render_template('pub.html')

    def post(self):
        from article_sql import db_operator
        db_operator.set(post_article_info())
        return redirect(url_for('list'))
app.add_url_rule('/pub/',view_func=Pubview.as_view('pub'))

@app.route('/')
def hello():
    return redirect(url_for('list'))

@app.route('/list/')
def list():
    from article_sql import db_operator
    articles = db_operator.get()
    return render_template('index.html', articles= articles)

@app.route('/author/<string:author>')
def author(author):
    from article_sql import db_operator
    articles = db_operator.get(author=author)
    return render_template('index.html', articles= articles)

@app.route('/content/<int:id>')
def content(id):
    from article_sql import db_operator
    article = db_operator.get(id)
    return render_template('content.html', article=article[0])

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    from article_sql import db_operator
    if flask.request.method == 'GET':
        article = db_operator.get(id)
        return render_template('eidt.html', article=article[0])

    if flask.request.method == 'POST':
        db_operator.set(post_article_info(), id)
        # modifier.modify(post_article_info(), id)
        return redirect(url_for('list'))

@app.route('/delete/<int:id>')
def delete(id):
    from article_sql import db_operator
    db_operator.delete(id)
    return redirect(url_for('list'))



if __name__ == '__main__':
    import article_sql
    app.run()
