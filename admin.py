import web
from web import form
from config import settings, db
import model
import json

urls = (
    '/', 'admin',
    '/login','login',
    '/logout', 'logout',
    '/site', 'site',
    '/page', 'page',
    '/page/add', 'edit_page',
    '/page/([^/]+)','edit_page',
    '/page/([^/]+)/delete','delete_page',
    '/page/([^/]+)/content', 'content',
    '/page/([^/]+)/content/add', 'edit_content',
    '/page/([^/]+)/content/(\d+)', 'edit_content',
    '/page/([^/]+)/content/(\d+)/delete', 'delete_content'
)
admin_app = web.application(urls, locals())

store = web.session.DBStore(db, 'sessions')
session = web.session.Session(admin_app, store, initializer={'logged_in': False})

render = web.template.render(settings.get('Settings','admin_templates'), base='layout')
plain = web.template.render(settings.get('Settings','admin_templates'))
def secure(f):
    def proxyfunc(self, *args, **kw):
        if session.logged_in:
            return f(self, *args, **kw)
        else:
            raise web.seeother("/login")
    return proxyfunc

class login:
    login_form = form.Form(
        form.Textbox("username", description="Username"),
        form.Password("password", description="Password"),
        form.Button("submit", type="submit", description="Login")
    )
    def GET(self):
        return plain.login("Login", self.login_form)

    def POST(self):
        data = self.login_form()
        if data.validates():
            d = data.d
            session.logged_in = model.login_user(d.username, d.password)
        raise web.seeother("/")

class logout:
    def GET(self):
        session.kill()
        raise web.seeother("/")

class site:
    site_form = form.Form(
        form.Textbox("ga", description="Google Analytics ID"),
        form.Textbox("title", description="Site Title"),
        form.Button("submit", type="submit", description="Save")
    )
    @secure
    def GET(self):
        site = model.get_site()
        if site:
            self.site_form.ga.set_value(site.ga)
            self.site_form.title.set_value(site.title)
        return render.form(u"Edit Site Properties", self.site_form)

    @secure
    def POST(self):
        data = self.site_form()
        if data.validates():
            site = model.get_site()
            if site:
                model.update_site(site.id, data.d.title, data.d.ga)
            else:
                model.add_site(data.d.title, data.d.ga)
        raise web.seeother('/site')

class page:
    @secure
    def GET(self):
        pages = model.get_pages(True)
        return render.pages(pages)

    @secure
    def POST(self):
        data = web.input()
        print data.data
        obj = json.loads(data.data)
        for pos in obj:
            model.update_page_pos(pos['name'],pos['pos'])
        raise web.seeother('/page')

class edit_page:
    page_form = form.Form(
        form.Textbox("name", description="Page Name"),
        form.Textbox("title", description="Page Title"),
        form.Textbox("position", description="Page Position"),
        form.Textbox("pagesize", description="Number of items per page"),
        form.Checkbox("draft", description="Is page in preview mode?" ),
        form.Button("submit", type="submit", description="Add")
    )
    @secure
    def GET(self, page=None):
        f = self.page_form()
        pg = model.get_page(page)
        if pg:
            f.name.set_value(pg.name)
            f.title.set_value(pg.title)
            f.position.set_value(pg.position)
            f.pagesize.set_value(pg.pagesize)
            f.draft.set_value(pg.draft)
        return render.page(f)

    @secure
    def POST(self, page=None):
        data = self.page_form()
        if data.validates():
            d = data.d
            cur = model.get_page(page)
            print d
            if cur:
                model.update_page(page, d.title, d.position, d.pagesize, int(d.draft))
            else:
                model.add_page(d.name, d.title, int(d.position), int(d.pagesize), int(d.draft))
        raise web.seeother('/page')

class delete_page:
    def GET(self,page):
        model.del_page(page)
        raise web.seeother('/page')

class content:
    @secure
    def GET(self, page):
        contents = model.get_all_page_contents(page)
        return render.page_content(page, contents)

class edit_content:
    content_form = form.Form(
        form.Textbox("title", description="Entry Title"),
        form.Checkbox("draft", description="Draft"),
        form.Textarea("content", description="Content", class_ = "entry", rows="40", cols="160"),
        form.Hidden("page"),
        form.Hidden("c_id"),
        form.Button("submit", type='submit', description="Save")
    )
    @secure
    def GET(self, page, content = None):
        c = model.get_content(content)
        f = self.content_form()
        if c:
            f.content.set_value(c.content)
            f.title.set_value(c.title)
            f.draft.set_value(c.draft)
        f.page.set_value(page)
        f.c_id.set_value(content)
        return render.edit_page_content(page, content, f)

    @secure
    def POST(self, page, c = None):
        data = self.content_form()
        if data.validates():
            d = data.d
            cur = model.get_content(d.c_id)
            if cur:
                model.update_content(d.c_id, d.page, d.title, d.content, int(d.draft))
            else:
                model.add_page_content(d.page, d.title, d.content, int(d.draft))
            raise web.seeother('/page/'+d.page+"/content")
        else:
            raise web.seeother('/page')

class delete_content:
    @secure
    def GET(selfself, page, content):
        model.del_page_content(content)
        raise web.seeother('/page/'+page+"/content")

class admin:
    @secure
    def GET(self):
        return render.home()