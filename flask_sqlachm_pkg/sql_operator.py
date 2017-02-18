#coding:utf8
from article_sql_table import db,Article,Author,Tag
from datetime import datetime

class Dboperator(object):
    def __init__(self, session):
        self.session = session

    def creator(self, cls):
        obj = cls()
        self.session.add(obj)
        return obj

    def set_author(func):
        def wapper(self, all_info, article_id = -1):
            authobj = self.session.query(Author).filter_by(author=all_info['author']).first() or self.creator(Author)
            authobj.author = all_info['author']
            self.session.commit()
            return func(self,all_info, article_id)
        return wapper

    def set_article(func):
        def wapper(self, all_info, article_id = -1):
            # 根据映射关系，创建文章一定是在创建作者之后
            authobj = self.session.query(Author).filter_by(author=all_info['author']).first()

            # 创建的时候用id=-1找不到就新建
            artcobj = self.session.query(Article).filter(Article.id==article_id).first() or self.creator(Article)

            artcobj.title = all_info['title']
            artcobj.content = all_info['content']
            artcobj.authorid = authobj.id
            artcobj.author = all_info['author']
            artcobj.time = datetime.now()
            self.unbound_manytomany(artcobj.tags)

            artcobj.tags += [self.session.query(Tag).filter_by(name=t).first() or Tag(name=t) for t in all_info['tag']]

            self.session.commit()
            return func(self, all_info, article_id)

        return wapper

    @set_author
    @set_article
    def set(self, all_info, article_id = -1):
        return

    def search_info(self, search_result):
        artilist = []
        for artiobj in search_result:
            dic_a = {}
            dic_a['id'] = artiobj.id
            dic_a['title'] = artiobj.title
            dic_a['author'] = artiobj.author
            dic_a['content'] = artiobj.content
            dic_a['time'] = artiobj.time
            dic_a['tag'] = [tag.name for tag in artiobj.tags]
            artilist.append(dic_a)
            # print 'title:%s  author:%s'%(dic_a['title'],dic_a['author'])
        return artilist

    def search_id(func):
        def wapper1(self, id = -1, *args, **kw):
            if id == -1:
                return func(self, *args, **kw)
            search_result = self.session.query(Article).filter_by(id=id).all()
            return self.search_info(search_result)
        return wapper1

    def search_author(func):
        def wapper(self, author='', *args, **kw):
            if author == '':
                return func(self, *args, **kw)
            search_result = self.session.query(Author).filter_by(author=author).first().bref
            return self.search_info(search_result)
        return wapper

    def search_all(func):
        def wapper(self):
            search_result = self.session.query(Article).all()
            return self.search_info(search_result)
        return wapper

    @search_id
    @search_author
    @search_all
    def get(self, id = -1, author =''):
        return

    def unbound_manytomany(self, boundlist):
        while boundlist:
            boundlist.pop()

    def delete(self, id):
        artiobj = self.session.query(Article).filter_by(id=id).first()
        self.unbound_manytomany(artiobj.tags)
        self.session.delete(artiobj)
        self.session.commit()

# db_operator = Dboperator(db.session)
def create_operator():
    return Dboperator(db.session)

