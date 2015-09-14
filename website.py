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

class home:
    def GET(self):
        raise web.seeother('/home')

class page:
    def GET(self, name, pg=0):
        page = model.get_page(name)
        pages = model.get_pages()
        if bool(page):
            content = self.__getContent(name)
            pgs = plain.pages(dict(page), pages)
            return render.page(dict(page), content, pgs)
        else:
            raise web.seeother('/home')

    def __getContent(self, name):
        content = StringIO.StringIO()
        markdown.markdownFromFile(input = settings.get("Settings", 'content') + name, output = content, extensions = ['markdown.extensions.extra', 'markdown.extensions.smarty'])
        return dict(render = content.getvalue())

if __name__ == "__main__":
    app.run()
