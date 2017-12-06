from Crypto.Cipher import AES
import sys
import os

def generate_skey():
  skey = os.urandom(16)
  return skey

def get_skey(kek, enckey):
  return decrypt(enckey[:16], kek, enckey[16:])

def gen_iv():
  return os.urandom(16)

def pad(msg):
  pad_length = 16-len(msg)%16
  return msg+chr(pad_length)*pad_length

def unpad(msg):
  return msg[:-ord(msg[-1])]

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

def recv_msg(conn, key):
  try:
    msg = conn.recv(1024)  
    if not msg:
      print >>sys.stderr, '[*] nothing from:', client_addr
    else:
      decrypted = decrypt(msg[:16], key, msg[16:])
      print >>sys.stderr, '[*] received dec: "%s"' % repr(decrypted)
    return decrypted
  except:
    print 'Error receiving message'
    exit(0)
