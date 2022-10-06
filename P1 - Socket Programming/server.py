import threading
import time
import random

import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    msg = "Welcome to CS 352!"
    csockid.send(msg.encode('utf-8'))
    client_data = csockid.recv(1000)
    message_from_client = client_data.decode('utf-8')
    print("[C]: Data received from server: {}".format(message_from_client))
    with open('./out-proj.txt', 'w') as f:
        f.write(message_from_client)
    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()