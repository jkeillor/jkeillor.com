create table page (
  name TEXT PRIMARY KEY,
  title TEXT,
  position INT,
  pagesize INT
);

create table content (
  id INTEGER PRIMARY KEY,
  page TEXT,
  title TEXT,
  created Date,
  updated Date,
  content TEXT
);
