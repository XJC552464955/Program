import socket

udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #udp套接字

udp_socket.sendto(b"haha",("192.168.36.1",8080))

udp_socket.close()