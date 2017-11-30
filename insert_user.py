#!/usr/bin/python

import psycopg2
import bcrypt

hostname = 'db.ist.utl.pt'
username = 'ist178876'
password = 'epiphone'
database = username

def insert(conn, username, password) :
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        cur.execute("insert into users values('" + username + "','"+hashed+"')")
        conn.commit()
    except:
        print "Unable to Insert user"
    
	
print "Using psycopg2"
try:
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
except:
   print "Unable to connect to database"
user = raw_input('username:')
pas = raw_input('password:')
insert(myConnection, user, pas)
myConnection.close()