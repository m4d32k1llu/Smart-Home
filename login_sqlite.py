#!/usr/bin/python
import getpass
import bcrypt

hostname = 'db.ist.utl.pt'
username = 'ist178876'
password = 'epiphone'
database = username

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT * FROM users" )

    for name, pas in cur.fetchall() :
        print name, pas

def Login(conn, username, password) :
    cur = conn.cursor()
    
    cur.execute( "SELECT * FROM users WHERE username = '" + username + "'")

    for name, pas in cur.fetchall() :
        if bcrypt.checkpw(password.encode('utf-8'), pas.encode('utf-8')):
	    return "Logged in as " + name
    return "Incorrect username or password"
	
print "Using sqlite3"
import sqlite3
myConnection = sqlite3.connect('smarthome.db')
user = raw_input('username:')
pas = getpass.getpass('password:')
#doQuery(myConnection)
print Login(myConnection, user, pas)
myConnection.close()
