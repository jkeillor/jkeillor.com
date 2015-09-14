#!/usr/bin/python
import web
from config import settings, db
import markdown
import StringIO
import admin
import model
urls = (
    '/admin', admin.admin_app,
    '/', 'home',
    '/([^/]+)', 'page',
    '/([^/]+)/(\d+)', 'page'
    )


web.config.debug = False
app = web.application(urls, locals())

render = web.template.render(settings.get('Settings','templates'), base='sidebar')
plain = web.template.render(settings.get('Settings', 'templates'))
extensions = ['markdown.extensions.extra', 'markdown.extensions.smarty']

class home:
    def GET(self):
        raise web.seeother('/home')

class page:
    def GET(self, name, pg=0):
        page = model.get_page(name)
        pages = model.get_pages()
        if bool(page):
            content = self.__getContent(page, pg)
            pgs = plain.pages(dict(page), pages)
            return render.page(dict(page), content, pgs)
        else:
            raise web.seeother('/home')

    def __getContent(self, page, offset):
        posts = model.get_page_contents(page.name, page.pagesize, offset)
        if posts:
            return [plain.post(x.title, markdown.markdown(x.content, extensions=extensions)) for x in list(posts)]
        else:
            return []

if __name__ == "__main__":
    app.run()
