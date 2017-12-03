from Crypto.Cipher import AES
import sys
import os

# confidentiality - from AES
# authentication  - from KEK
# freshness       - from challenge
# integrity       - from "CBC-MAC"
# perfect forward secrecy - no

def generate_skey():
  skey = os.urandom(32)
  return skey

def get_skey(kek, enckey):
  return decrypt(enckey[:16], kek, enckey[16:])

def gen_iv():
  return os.urandom(16)

#### leave it, will be used for fridge
def pad(msg):
  pad_length = 16-len(msg)%16
  return msg+chr(pad_length)*pad_length

def unpad(msg):
  return msg[:-ord(msg[-1])]
####

def encrypt(iv, key, msg):
  msg = pad(msg)
  cipher = AES.new(key,AES.MODE_CBC,iv)
  encrypted = cipher.encrypt(msg)
  return encrypted

def decrypt(iv, key, msg):
  cipher = AES.new(key,AES.MODE_CBC,iv)
  decrypted = cipher.decrypt(msg)
  decrypted = unpad(decrypted)
  return decrypted

def send_msg(conn, iv, key, msg):
  encrypted = encrypt(iv, key, msg)
  msg = iv + encrypted
  print >>sys.stderr, '[*] sending:  "%s"' % repr(msg)
  conn.sendall(msg)
  return

def recv_msg(conn, key):#, mac=False):
  try:
    msg = conn.recv(1024)  
    if not msg:
      print >>sys.stderr, '[*] nothing from:', client_addr
    else:
      decrypted = decrypt(msg[:16], key, msg[16:])
    #  print >>sys.stderr, '[*] received: "%s"' % repr(msg)
      print >>sys.stderr, '[*] received dec: "%s"' % repr(decrypted)
    # if mac:
    #   newiv = msg[:16]
    #   newmsg = msg[16:]
    #   newenc = encrypt(newiv, key, newmsg)
    #   print "[*] mac checking ["+repr(msg[16:])+"] == ["+repr(newmsg)+"]"
    #   if msg[16:] == newmsg:
    #     print "[*] mac ok"
    #     return decrypted
    #   else:
    #     print "[*] mac failed"
    #     return -1 # code for integrity failed
    return decrypted
  except:
    print 'Error receiving message'
    exit(0)
