create table if not exists page (
  name TEXT UNIQUE PRIMARY KEY,
  title TEXT,
  position INT,
  pagesize INT,
  draft INT
);

create table if not exists content (
  id INTEGER PRIMARY KEY,
  page TEXT,
  title TEXT,
  created Date,
  updated Date,
  content TEXT,
  draft INT
);
create table if not exists link (
  id INTEGER PRIMARY KEY,
  ref TEXT,
  url TEXT
);

create table if not exists site (
  title TEXT,
  ga TEXT);

create table if not exists user (
  username TEXT UNIQUE PRIMARY KEY,
  password TEXT
);

create table if not exists sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);