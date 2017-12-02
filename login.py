#!/usr/bin/python

import bcrypt

hostname = 'db.ist.utl.pt'
username = 'ist178876'
password = 'epiphone'
database = username

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT nome FROM categoria" )

    for name in cur.fetchall() :
        print name

def Login(conn, username, password) :
    cur = conn.cursor()
    
    cur.execute( "SELECT * FROM users WHERE username = '" + username + "'")

    for name, pas in cur.fetchall() :
        if bcrypt.checkpw(password, pas):
	    return "Logged in as " + name
    return "Incorrect username or password"
	
print "Using psycopg2"
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
user = raw_input('username:')
pas = raw_input('password:')
print Login(myConnection, user, pas)
myConnection.close()
