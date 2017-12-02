import socket
import sys
import os
import ssl
import lamp
import time

TCP_IP = '192.168.2.1'
TCP_PORT = 12345

prompt = "[HomeMgr: insert a command]>> "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (TCP_IP,TCP_PORT)
print >>sys.stderr, '[G] listening on: %s; port: %s' % server_addr
sock.bind(server_addr)

sock.listen(1)

# accept the connection
while True:
  # Wait for a connection
  print >>sys.stderr, '[G] waiting for a connection'
  conn, client_addr = sock.accept()
  ssl_conn = ssl.wrap_socket(conn,
                               server_side=True,
                               certfile="server.crt",
                               keyfile="server.key")
  try:
    print >>sys.stderr, '[G] connected to:', client_addr

    # authentication

    # if wrong, drop connection

    # if correct, do nothing
  
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
        break
      elif command == "help" or command == "?":
        ssl_conn.sendall("valid commands: [help, exit, lamp on, lamp off, fridge show]")
      elif command == "exit" or command == "q":
        ssl_conn.sendall("exiting...")
        break
      else:
        ssl_conn.sendall("ERROR: command not found: input ? for help")
      time.sleep(1)
      
  finally:
    print '[G] closing connection to:', client_addr
    ssl_conn.close()
