#!/usr/bin/python
import web
import ConfigParser
import markdown
import StringIO


urls = (
    '/', 'home',
    '/([^/]+)', 'page',
    '/([^/]+)/(\d+)', 'page'
    )
web.config.debug = True
app = web.application(urls, globals())
config = ConfigParser.SafeConfigParser()
config.read('./app.cfg')
db = web.database(dbn='sqlite', db=config.get('Settings', 'db'))
render = web.template.render(config.get('Settings','templates'), base='sidebar')
plain = web.template.render(config.get('Settings', 'templates'))

class home:
    def GET(self):
        raise web.seeother('/home')

class page:
    def GET(self, name, pg=0):
        page = db.select('page', vars=dict(name = name), where="name = $name", limit = 1)
        pages = [dict(title = x.title, name= x.name) for x in list(db.select('page', what = "title, name"))]
        if bool(page):
            p = list(page).pop()
            content = self.__getContent(name)
            pgs = plain.pages(dict(p), pages)
            return render.page(dict(p), content, pgs)
        else:
            raise web.seeother('/home')

    def __getContent(self, name):
        content = StringIO.StringIO()
        markdown.markdownFromFile(input = config.get("Settings", 'content') + name, output = content, extensions = ['markdown.extensions.extra', 'markdown.extensions.smarty'])
        return dict(render = content.getvalue())

if __name__ == "__main__":
    app.run()
