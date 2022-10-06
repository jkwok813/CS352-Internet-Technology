import threading
import time
import random
import socket
import sys
import select

def client():
    try:
        cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port1 = int(sys.argv[3])
    localhost_addr1 = socket.gethostbyname(sys.argv[2])
    port2 = int(sys.argv[5])
    localhost_addr2 = socket.gethostbyname(sys.argv[4])

    # connect to the server on local machine
    server_binding1 = (localhost_addr1, port1)
    server_binding2 = (localhost_addr2, port2)
    cs1.connect(server_binding1)
    cs2.connect(server_binding2)
    print("Clients succesfully connected")
    rs_listen_port = int(sys.argv[1])
    server_binding3 = ('', rs_listen_port)
    ss.bind(server_binding3)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))
    input = [cs1, cs2]

    # Receive data from the server
    counter = 1
    while counter == 1:
        if csockid.fileno() == -1:
		sys.exit(0)
        data_from_client = csockid.recv(1000)
        server_string = data_from_client.decode('utf-8')
        print("Client: " + server_string)
        cs1.send(server_string.encode('utf-8'))
        cs2.send(server_string.encode('utf-8'))
        inputready, outputready, exceptready = select.select(input, [], [], 5.0)
        if exceptready != []:
            print("Error")
            exit()
        if inputready != []:
            s = inputready[0]
            data = s.recv(1000)
            response = data.decode('utf-8')
            print("TS " + response)
            csockid.send(response.encode('utf-8'))
        else:
            response = data_from_client + " - TIMED OUT\n"
            csockid.send(response.encode('utf-8'))

    ss.close()
    cs1.close()
    cs2.close()
    exit()


if __name__ == "__main__":
    t1 = threading.Thread(name='client', target=client)
    t1.start()



