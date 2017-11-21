#!/usr/bin/python

hostname = 'db.ist.utl.pt'
username = 'ist178876'
password = 'epiphone'
database = username

def insert(conn, username, password) :
    cur = conn.cursor()

    cur.execute( "insert into users values('" + username + "','"+password"')")

    for name, pas in cur.fetchall() :
        if(username == name and pas == password):
	    return "Logged in"
    return "Incorrect username or password"
	
print "Using psycopg2"
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
user = raw_input('username:')
pas = raw_input('password:')
print inset(myConnection, user, pas)
myConnection.close()
