#!/usr/bin/python

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


print "Using psycopg2"
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()