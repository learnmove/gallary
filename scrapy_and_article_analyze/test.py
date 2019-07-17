# -*- coding: utf-8 -*-

import sqlite3 as sql


db = sql.connect('test.db')

cs = db.cursor()

cs.execute("select type from urls")
Set = cs.fetchall()
Set = set(Set)
