import socket
import sys
import os
import ssl
import fridge
import lamp
import time
import bcrypt
import sqlite3

TCP_IP = '192.168.2.1'
TCP_PORT = 12345

def Login(conn, username, password) :
    cur = conn.cursor()
    data = (username,) 
    cur.execute( "SELECT * FROM users WHERE username = ?", data)

    for name, pas in cur.fetchall() :
        if bcrypt.checkpw(password.encode('utf-8'), pas.encode('utf-8')):
	    return True
    return False

	
prompt = "[HomeMgr: insert a command]>> "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (TCP_IP,TCP_PORT)
print >>sys.stderr, '[G] listening on: %s; port: %s' % server_addr
sock.bind(server_addr)

sock.listen(1)

while True:
  # Wait for a connection
  print >>sys.stderr, '[G] waiting for a connection'
  conn, client_addr = sock.accept()
  ssl_conn = ssl.wrap_socket(conn,
                               server_side=True,
                               certfile="server.crt",
                               keyfile="server.key")
  ssl_conn.settimeout(60)
  try:
    print >>sys.stderr, '[G] connected to:', client_addr
    myConnection = sqlite3.connect('../smarthome.db')
    # authentication

    # if wrong, drop connection

    # if correct, do nothing
    # send prompt
    msg = "Please Log In"
    print >>sys.stderr, '[G] sending:  "%s"' % repr(msg)
    ssl_conn.sendall(msg)

    # receive command 
    command = ssl_conn.recv(1024)
    print "[G] received command:", command
    data = command.split()
    if len(data) != 3 or data[0] != "login":
        print "Login data received from sever was badly formated."
        print "Closing server connection..."
        msg = "ERROR login"
        ssl_conn.sendall(msg)
    elif not Login(myConnection, data[1], data[2]):
        msg = "Login Failed"
        print msg
        ssl_conn.sendall(msg)
    else:
        msg = "Login True"
        print msg
        ssl_conn.sendall(msg)  
        command = ssl_conn.recv(1024)
        print "[G] received:", command
        
        while True:
            # send prompt
            msg = prompt
            print >>sys.stderr, '[G] sending:  "%s"' % repr(msg)
            ssl_conn.sendall(msg)

    	    # receive command 
     	    command = ssl_conn.recv(1024)
            print "[G] received command:", command
      
            # print
            # command = raw_input("[HomeMgr: insert a command]>> ")
            if command == "lamp on":
                lamp.client("1")
                ssl_conn.sendall("lamp on")
            elif command == "lamp off":
                lamp.client("0")
                ssl_conn.sendall("lamp off")
            elif command == "fridge show":
                fridge_msg = fridge.client("0")
                ssl_conn.sendall(fridge_msg)
            elif command == "fridge temp":
              fridge_message = fridge.client("1")
              ssl_conn.sendall(fridge_message)
            elif command == "fridge raise t":
              fridge_message = fridge.client("2")
              ssl_conn.sendall(fridge_message)        
            elif command == "fridge lower t":
              fridge_message = fridge.client("3")
              ssl_conn.sendall(fridge_message)
            elif command == "help" or command == "?":
              ssl_conn.sendall("valid commands: [help, exit, lamp on, lamp off, fridge show, fridge temp, fridge raise t, fridge lower t]")
            elif command == "exit" or command == "q":
                ssl_conn.sendall("exiting...")
                break
            else:
                ssl_conn.sendall("ERROR: command not found: input ? for help")
            time.sleep(1)

  except socket.error, e:
    print "[G] CATCHED:", e
    ssl_conn.close()
    continue
  
  finally:
    print '[G] closing connection to:', client_addr
    ssl_conn.close()
