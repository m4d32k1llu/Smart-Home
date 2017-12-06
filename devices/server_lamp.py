import socket
import sys
import os
from crypt import *

TCP_IP = '192.168.3.10'
TCP_PORT = 31415

KEK = "0123456789abcdef"

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
      expected_resp = nounce - 1 
      send_msg(conn, iv, skey, format(nounce,'x'))
      print "[S] challenge sent:", nounce
      
      # receive challenge response + request
      response1 = recv_msg(conn, skey)
      chall_resp = response1[0:8]
      sanity = response1[8:16]
      request = response1[16:]
      if int(chall_resp,16) != expected_resp or not all(b == "0" for b in sanity) or not all(b == "1" for b in request[8:]) or len(request) > 16:
        print '[S] integrity breached, rejecting request from:', client_addr
        conn.close()
        continue
      
      # send response
      new_state = request[7]
      if new_state == "1":
        print "[S] turning on the light"
      elif new_state == "0":
        print "[S] turning off the light"
      else:
        print "[S] unrecognized option", repr(new_state)
      iv = gen_iv()
      response2 = "DEBUG server received: [" +  response1 + "] with new state [" + new_state + "]"
      send_msg(conn, iv, skey, response2)
               
    except socket.error, e:
      print "[S] exception catched",e
      conn.close()
      
    finally:
      print '[S] closing connection to:', client_addr
      conn.close()

if __name__ == "__main__":
  server()
