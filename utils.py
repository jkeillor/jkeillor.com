#!/usr/bin/python

import sqlite3
import ConfigParser
import argparse
import bcrypt
from config import settings, db
import model

parser = argparse.ArgumentParser(description="Website setup utilities")
parser.add_argument("--user", help = 'username')
parser.add_argument("--pw", help="password")
parser.add_argument("--page", help = 'page name')
parser.add_argument("--title", help = 'page title')
parser.add_argument("--position", help = 'page position')
args = parser.parse_args()

def make_user(username, password):
    existing = model.get_user(username)
    if existing:
        print "Updating existing user"
        model.update_user(username, password)
    else:
        print "Creating new user"
        model.add_user(username, password)

def make_page(page, title, position):
    model.add_page(page,title, position, draft=0)

if args.user:
    make_user(args.user, args.pw)
if args.page:
    make_page(args.page, args.title, args.position)
