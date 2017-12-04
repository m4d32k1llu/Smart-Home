#!/usr/bin/python
import getpass
import psycopg2
import bcrypt

hostname = 'db.ist.utl.pt'
username = 'ist178876'
password = 'epiphone'
database = username

def Login(conn, username, password) :
    cur = conn.cursor()
    
    cur.execute( "SELECT * FROM users WHERE username = '" + username + "'")

    for name, pas in cur.fetchall() :
        if bcrypt.checkpw(password, pas):
	    return True
    return False
	
def insert(conn, username, password) :
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    data = (username, hashed)
    try:
        cur.execute("insert into users values(%s,%s)", data)
        conn.commit()
    except:
        print "Unable to Insert user"
    
	
print "Please input super user password..."
try:
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
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
