#coding:utf8
import flask
from flask import Flask,render_template,url_for,redirect

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Chiloon@localhost:3306/a?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from dbpkg import init_app,get_operator
init_app(app)
operator = get_operator()


def post_article_info():
    article = {}
    article['title'] = flask.request.form.get('title')
    article['author'] = flask.request.form.get('author')
    article['content'] = flask.request.form.get('content')
    article['tag'] = flask.request.form.getlist('tag')
    return article


@app.route('/')
def hello():
    return redirect(url_for('list'))

@app.route('/list/')
def list():
    articles = operator.get()
    return render_template('index.html', articles=articles)

@app.route('/pub/', methods=['GET', 'POST'])
def pub():
    if flask.request.method == 'GET':
        return render_template('pub.html')

    if flask.request.method == 'POST':
        operator.set(post_article_info())
        return redirect(url_for('list'))

@app.route('/author/<string:author>')
def author(author):
    articles = operator.get(author=author)
    return render_template('index.html', articles=articles)

@app.route('/content/<int:id>')
def content(id):
    article = operator.get(id)
    return render_template('content.html', article=article[0])

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if flask.request.method == 'GET':
        article = operator.get(id)
        return render_template('eidt.html', article=article[0])

    if flask.request.method == 'POST':
        operator.set(post_article_info(), id)
        return redirect(url_for('list'))

@app.route('/delete/<int:id>')
def delete(id):
    operator.delete(id)
    return redirect(url_for('list'))
#
#
# class app_loader(object):
#     def __init__(self):
#         self.app = Flask(__name__)
#
#     def create_operator(self):
#         self.oper = create_operator()
#         self.loadviews()
#
#     def loadviews(self):
#         oper = [self.oper]
#         @self.app.route('/')
#         def hello():
#             # return '%s'%url_for('list')
#             return redirect(url_for('list'))
#
#         @self.app.route('/list/')
#         def list():
#             articles = oper[0].get()
#             return render_template('index.html', articles=articles)
#
#         @self.app.route('/pub/', methods=['GET', 'POST'])
#         def pub():
#             if flask.request.method == 'GET':
#                 return render_template('pub.html')
#
#             if flask.request.method == 'POST':
#                 oper[0].set(post_article_info())
#                 return redirect(url_for('list'))
#
#         @self.app.route('/author/<string:author>')
#         def author(author):
#             articles = oper[0].get(author=author)
#             return render_template('index.html', articles=articles)
#
#         @self.app.route('/content/<int:id>')
#         def content(id):
#             article = oper[0].get(id)
#             return render_template('content.html', article=article[0])
#
#         @self.app.route('/edit/<int:id>', methods=['GET', 'POST'])
#         def edit(id):
#             if flask.request.method == 'GET':
#                 article = oper[0].get(id)
#                 return render_template('eidt.html', article=article[0])
#
#             if flask.request.method == 'POST':
#                 oper[0].set(post_article_info(), id)
#                 return redirect(url_for('list'))
#
#         @self.app.route('/delete/<int:id>')
#         def delete(id):
#             oper[0].delete(id)
#             return redirect(url_for('list'))
#
#
#     def __call__(self, *args, **kwargs):
#         return self.app
#
# if __name__ == '__main__':
#     app = app_loader()
#     with app().app_context():
#         installapp(app())
#         app.create_operator()
#     app().run()