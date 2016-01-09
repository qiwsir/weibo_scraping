#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('weibo.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE rentings (post_id TEXT PRIMARY KEY, post_text TEXT,
          url TEXT, post_date INTEGER)''')

# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
