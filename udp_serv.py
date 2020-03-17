import socket
udp_ip = '127.0.0.1'
udp_port = 8014
fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fd.bind((udp_ip,udp_port))
while True:
    r = fd.recvfrom(10000)
    if (str(r[0].decode('utf-8')) == '---exit---'):
        break
    elif (str(r[0].decode('utf-8')) == 'message'):
        mess = fd.recvfrom(10000)
        print("client : %s"%(r[0]))
        reply = mess[0]
        client_address = mess[1]
        fd.sendto(reply, client_address)
    elif (str(r[0].decode('utf-8')) == 'file'):
        data = fd.recvfrom(10000)
        file_name = str(data[0].decode('utf-8'))
        fd.sendto(data[0], client_address)
        file = open(file_name, "wb")

        data = fd.recvfrom(10000)
        file_buffer = data[0]
        fd.sendto(file_buffer, client_address)
        file.write(file_buffer)
        file.close()


fd.close()