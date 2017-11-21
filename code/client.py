import socket
import sys
import os
from crypt import *

TCP_IP = 'localhost'
TCP_PORT = 31415

KEK = "0123456789abcdef"
#INTEGRITY_KEY = "thisstheintegkey"
INFO_BYTE = 13

state = "1" # 0 -> turn off light; 1 -> turn on light

def client():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_addr = (TCP_IP,TCP_PORT)
  print >>sys.stderr, '[C] connecting to: %s; port: %s' % client_addr
  sock.connect(client_addr)

  try:
    # send session key and check freshness
    iv = gen_iv()
    skey = generate_skey()
    send_msg(sock, iv, KEK, skey)
    print '[C] sent session key:', repr(skey)
    chall = recv_msg(sock, skey)
    print "[C] received challenge:", int(chall,16)
    chall_resp = format(int(chall,16) - 1,'x')
    iv = gen_iv()
    send_msg(sock, iv, skey, chall_resp)
    print "[C] sent challenge response:", int(chall_resp,16)
    
    # send data
    iv = gen_iv()
    #state = "1" # 0 -> turn off light; 1 -> turn on light
    message = os.urandom(INFO_BYTE) + state + os.urandom(16 - INFO_BYTE - 1)# + INTEGRITY_KEY
    send_msg(sock, iv, skey, message)
    print "[C] sent plaintext", repr(message)

    # receive response
    response = recv_msg(sock, skey)
    print '[C] response: "%s"' % repr(response)

  finally:
    print >>sys.stderr, '[C] closing socket'
    sock.close()

if __name__ == "__main__":
  client()
