import datetime
from config import db
import bcrypt


#####################
# Site Operations   #
#####################
def get_site():
    try:
        return db.select('site', limit = 1)[0]
    except IndexError:
        None

def update_site(id, title, ga):
    db.update('site', where = "id=$id", vars=locals(), title = title, ga = ga)

def add_site(title, ga):
    db.insert('site', title=title, ga=ga)

###########################
# Link Operations   #
###########################
def get_links():
    return [dict(id= x.id, ref=x.ref, url = x.url) for x in list(db.select('links', what = "ref, url", vars = locals()))]

def add_link(ref, url):
    db.insert('link', ref=ref, url=url)

def del_link(id):
    db.delete('link', where="id=$id", vars = locals())

def update_link(id, ref, url):
    db.update('link', where="id=$id", vars=locals(), ref=ref, url=url)


#####################
# Page Operations   #
#####################
def get_pages(drafts=False):
    order = "position ASC"
    if drafts:
        return [dict(title = x.title, name= x.name) for x in list(db.select('page',
            what = "title, name", order=order))]
    else:
        return [dict(title = x.title, name= x.name) for x in list(db.select('page',
            what = "title, name", where="draft = $drafts", vars = dict(drafts = int(drafts)), order=order))]

def get_page(name):
    try:
        return db.select('page', vars=dict(name = name), where="name = $name", limit = 1)[0]
    except IndexError:
        None

def add_page(name, title, position, pagesize = 10, draft = 1):
    db.insert('page', name = name, title=title, position = position, pagesize = pagesize, draft = draft)

def del_page(name):
    db.delete('page', where="name = $name", vars = locals())

def update_page(name, title, position, pagesize = 10, draft = 1):
    db.update('page', where="name=$name", vars=locals(),
        title = title, position = position, pagesize = pagesize, draft = draft)

def update_page_pos(name, position):
    db.update("page", where="name=$name", vars=locals(), position = position)

############################
# Page Content operations  #
############################
def get_page_contents(pg_name, pg_size, offset=0, drafts=False):
    return db.select('content', where="page=$pg and draft=$d", vars = dict(pg=pg_name, d=int(drafts)), offset=offset, limit=pg_size, order="created DESC")

def get_all_page_contents(pg_name):
    return db.select('content', where="page=$pg_name", vars = locals())

def get_content(id):
    try:
        return db.select('content', where="id = $id", vars = locals())[0]
    except IndexError:
        None

def update_content(id, page, title, content, draft = 1):
    db.update('content', where="id=$id", vars=locals(), page = page,
        title = title, content = content, updated = datetime.datetime.utcnow(), draft = draft)

def add_page_content(page, title, content, draft = 1):
    d = datetime.datetime.utcnow()
    db.insert('content', page = page, title = title, content = content, updated = d, created = d, draft=draft)

def del_page_content(content):
    db.delete('content', where="id=$content", vars=locals())

############################
# User Operations          #
############################
#
#    print username
#    print password
#    conn = sqlite3.connect(settings.get('Settings', 'db'))
#    c = conn.cursor()
#    c.execute('select * from user where username=?', (username,))
#    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#
#    if c.fetchone():
#        print "User already exists, updating password"
#        c.execute("update user set password=? where username=?", (hashed, username) )
#    else:
#        print "Adding new user"
#        c.execute("insert into user values (?, ?)", (username, hashed))
#
#    conn.commit()
#    conn.close()
def add_user(username, password):
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    db.insert("user", password = hash, username = username)

def get_user(username):
    try:
        return db.select("user", where="username=$username", vars = locals())[0]
    except IndexError:
        None

def update_user(username, password):
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    db.update("user", where = "username=$username", vars = locals(), password=hash)

def del_user(username):
    db.delete('user', where = "username=$username", vars=locals())

def login_user(username, password):
    user = get_user(username)
    if user:
        return bcrypt.hashpw(password, user.password) == user.password
    else:
        return False