import socket
import sys
import os
from crypt import *

TCP_IP = '192.168.3.10'
TCP_PORT = 31415

KEK = "0123456789abcdef"
INTEGRITY_KEY = "thisstheintegkey"
INFO_BYTE = 13

def server():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_addr = (TCP_IP,TCP_PORT)
  print >>sys.stderr, '[S] listening on: %s; port: %s' % server_addr
  sock.bind(server_addr)

  sock.listen(1)
  while True:
    # Wait for a connection
    print >>sys.stderr, '[S] waiting for a connection'
    conn, client_addr = sock.accept()
    try:
      print >>sys.stderr, '[S] connected to:', client_addr
      
      # get session key and check freshness
      skey = recv_msg(conn, KEK)
      print '[S] received session key:', repr(skey)
      iv = gen_iv()
      nounce = int(os.urandom(4).encode('hex'),16)
      send_msg(conn, iv, skey, format(nounce,'x'))
      print "[S] challenge sent:", nounce
      response = int(recv_msg(conn, skey),16)
      print "[S] challenge response received:", response
      if response != nounce - 1:
        print "[S] challenge failed, closing connection"
        conn.close()
        continue
      else:
        print "[S] challenge accomplished, continue"
        
      # receive message
      msg = recv_msg(conn, skey)#, True)
      integrity_block = msg[:16]
      info_block = msg[16:32]
      if integrity_block != INTEGRITY_KEY or not all(b == "0" for b in info_block[8:13]):
      # if msg == -1:
        print '[S] integrity breached, rejecting request from:', client_addr
        conn.close()
        continue
      
      # send response
      new_state = info_block[INFO_BYTE]
      if new_state == "1":
        print "[S] turning on the light"
      elif new_state == "0":
        print "[S] turning off the light"
      else:
        print "[S] unrecognized option", repr(new_state)
      iv = gen_iv()
      response = "DEBUG server received: [" +  msg + "] with new state [" + new_state + "]"
      send_msg(conn, iv, skey, response)
    except:
      print "[S] exception catched"
      conn.close()
      
    finally:
      print '[S] closing connection to:', client_addr
      conn.close()

if __name__ == "__main__":
  lampQ = True
  fridgeQ = False

  server()
