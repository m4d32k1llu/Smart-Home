import socket
import sys
import os
from crypt import *

TCP_IP = '192.168.3.10'
TCP_PORT = 31415

KEK = "0123456789abcdef"
INTEGRITY_KEY = "thisstheintegkey"
INFO_BYTE = 13

def client(state):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_addr = (TCP_IP,TCP_PORT)
  print >>sys.stderr, '[L] connecting to: %s; port: %s' % client_addr
  sock.connect(client_addr)

  try:
    # send session key and check freshness
    iv = gen_iv()
    skey = generate_skey()
    send_msg(sock, iv, KEK, skey)
    print '[L] sent session key:', repr(skey)
    chall = recv_msg(sock, skey)
    print "[L] received challenge:", int(chall,16)
    chall_resp = format(int(chall,16) - 1,'x')
    iv = gen_iv()
    send_msg(sock, iv, skey, chall_resp)
    print "[L] sent challenge response:", int(chall_resp,16)
    
    # send data
    iv = gen_iv()
    message = INTEGRITY_KEY + os.urandom(INFO_BYTE - 7) + "0000000" + state + os.urandom(16 - INFO_BYTE - 1)
    send_msg(sock, iv, skey, message)
    print "[L] sent plaintext", repr(message)

    # receive response
    response = recv_msg(sock, skey)
    print '[L] response: "%s"' % repr(response)

  finally:
    print >>sys.stderr, '[L] closing socket'
    sock.close()

if __name__ == "__main__":
  state = "0" # 0 -> turn off light; 1 -> turn on light
  client(state)
