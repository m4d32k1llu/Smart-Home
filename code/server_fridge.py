import socket
import sys
import os
from crypt import *
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

TCP_IP = 'localhost'
TCP_PORT = 31414

KEK = "0123456789abcdef"
INTEGRITY_KEY = "thisstheintegkey"
INFO_BYTE = 13

def server():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_addr = (TCP_IP,TCP_PORT)
  print >>sys.stderr, '[F] listening on: %s; port: %s' % server_addr
  sock.bind(server_addr)

  sock.listen(1)
  while True:
    # Wait for a connection
    print >>sys.stderr, '[F] waiting for a connection'
    conn, client_addr = sock.accept()
    try:
      print >>sys.stderr, '[F] connected to:', client_addr
      
      # eke-rsa
      key_msg = recv_msg(conn,KEK)
      print "received public key",repr(key_msg)
      public_key = RSA.importKey(key_msg)
      skey = generate_skey()
      print "[F] generated session key:", repr(skey)
      encrypted_skey = public_key.encrypt(skey, 32)[0]
      print "[F] sending encrypted session key:", repr(encrypted_skey)
      iv = gen_iv()
      send_msg(conn, iv, KEK, encrypted_skey)

      # challenge response
      ## receive challenge1
      chall1 = int(recv_msg(conn, skey),16)
      print "[F] received challenge1:", chall1
      ## send response1 and challenge2
      resp1 = chall1 - 1
      chall2 = int(os.urandom(4).encode('hex'),16)
      iv = gen_iv()
      print "[F] sending response1:", resp1
      print "[F] sending challenge2:", chall2
      b2 = format(resp1,'x') + format(chall2,'x')
      send_msg(conn, iv, skey, b2)
      ## receive response2
      resp2 = int(recv_msg(conn, skey),16)
      print "[F] challenge2 response received:", resp2
      if resp2 != chall2 - 1:
        print "[F] challenge failed, closing connection"
        conn.close()
        continue
      else:
        print "[F] challenge accomplished, continue"  
      
      # receive message
      msg = recv_msg(conn, skey)#, True)
      integrity_block = msg[:16]
      info_block = msg[16:32]
      if integrity_block != INTEGRITY_KEY or not all(b == "0" for b in info_block[8:13]):
      # if msg == -1:
        print '[F] integrity breached, rejecting request from:', client_addr
        conn.close()
        continue
      
      # send response
      new_state = info_block[INFO_BYTE]
      if new_state == "0":
        print "[F] got option 0"
      else:
        print "[F] unrecognized option", repr(new_state)
      iv = gen_iv()
      response = "Fridge has: 3 yogurt, 2 milk, 1 cheese, 5 ham"
      send_msg(conn, iv, skey, response)
    except:
      print "[F] exception catched - Unexpected error:", sys.exc_info()[0]
      conn.close()
      
    finally:
      print '[F] closing connection to:', client_addr
      conn.close()

if __name__ == "__main__":
  server()
