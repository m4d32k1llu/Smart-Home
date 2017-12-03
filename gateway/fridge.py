import socket
import sys
import os
from crypt import *
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

TCP_IP = '192.168.3.100'
TCP_PORT = 31414

KEK = "0123456789abcdef"
INTEGRITY_KEY = "thisstheintegkey"
INFO_BYTE = 13

def client(state):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_addr = (TCP_IP,TCP_PORT)
  print >>sys.stderr, '[R] connecting to: %s; port: %s' % client_addr
  sock.connect(client_addr)

  try:
    # eke-rsa
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    publickey = rsa_key.publickey().exportKey("DER")
    print "[R] sending public key:", repr(publickey)
    iv = gen_iv()
    send_msg(sock,iv,KEK,publickey)
    enc_skey = recv_msg(sock,KEK)
    print "[R] received encrypted session key:", repr(enc_skey)
    skey = rsa_key.decrypt(enc_skey)
    print "[R] obtained session key:", repr(skey)

    # challenge response
    ## send challenge1
    chall1 = int(os.urandom(4).encode('hex'),16)
    print "[R] sending challenge1", chall1
    iv = gen_iv()
    send_msg(sock,iv,skey,format(chall1,'x'))
    ## receive response1 and challenge2
    temp = recv_msg(sock, skey)
    resp1 = int(temp[0:8],16)
    print "[R] received response1:",resp1
    if resp1 != chall1 - 1:
      print "[R] challenge failed, closing connection"
      sock.close()
    else:
      print "[R] challenge accomplished, continue"
    chall2 = int(temp[8:],16)
    print "[R] received challenge2:", chall2
    ## send response2
    resp2 = chall2 - 1
    iv = gen_iv()
    send_msg(sock, iv, skey, format(resp2,'x'))
    print "[R] sent response2:", resp2
    
    # send data
    iv = gen_iv()
    message = INTEGRITY_KEY + os.urandom(INFO_BYTE - 5) + "00000" + state + os.urandom(16 - INFO_BYTE - 1)
    send_msg(sock, iv, skey, message)
    print "[R] sent plaintext", repr(message)

    # receive response
    response = recv_msg(sock, skey)
    print '[R] response: "%s"' % repr(response)

  finally:
    print >>sys.stderr, '[R] closing socket'
    sock.close()
    return response

if __name__ == "__main__":
  state = "0" # 0 -> get info
  client(state)
