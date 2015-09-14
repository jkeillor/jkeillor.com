__author__ = 'jkeillor'
import web
import ConfigParser

settings = ConfigParser.SafeConfigParser()
settings.read('./app.cfg')
db = web.database(dbn='sqlite', db=settings.get('Settings', 'db'))
