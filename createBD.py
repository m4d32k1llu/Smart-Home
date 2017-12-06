import sqlite3

sql = open('users.sql', 'r').read()
#print sql
conn = sqlite3.connect('smarthome.db')
cur = conn.cursor()
cur.executescript(sql)
conn.commit()
cur.close()
conn.close()
