import socket
import ssl
import sys

TCP_IP = '192.168.2.1'
TCP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_addr = (TCP_IP,TCP_PORT)

ssl_sock = ssl.wrap_socket(sock,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)

print >>sys.stderr, '[C] connecting to: %s; port: %s' % client_addr
ssl_sock.connect(client_addr)

try:
  while True:
    r = ssl_sock.recv(1024)
    print "[C] received:", r

    s = raw_input()
    print "[C] sending:", s
    ssl_sock.sendall(s)

    r = ssl_sock.recv(1024)
    print "[C] received answer:", r
    
    if s == "q" or s == "exit":
      break
  
finally:
  print >>sys.stderr, '[C] closing socket'
  ssl_sock.close()
