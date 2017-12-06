#!/usr/bin/python
import getpass
import sqlite3
import bcrypt

def Login(conn, username, password) :
    cur = conn.cursor()
    
    cur.execute( "SELECT * FROM users WHERE username = '" + username + "'")

    for name, pas in cur.fetchall() :
        if bcrypt.checkpw(password.encode('utf-8'), pas.encode('utf-8')):
	    return True
    return False
	
def insert(conn, username, password) :
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    data = (username, hashed)
    print data
    try:
        cur.execute("insert into users values(?,?)", data)
        conn.commit()        
    except:
        print "Unable to Insert user"
    
	
print "Please input super user password..."
try:
    myConnection = sqlite3.connect('smarthome.db')
except:
    print "Unable to connect to database"
pas = getpass.getpass('password:')
if not Login(myConnection, "super", pas):
    print "Incorrect password"
else:
    print "Type new user settings..."
    user = raw_input('username:')
    pas = getpass.getpass('password:')
    insert(myConnection, user, pas)
myConnection.close()
