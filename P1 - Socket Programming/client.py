import threading
import time
import random

import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server = cs.recv(1000)
    server_string = data_from_server.decode('utf-8')
    result_string = ""
    with open('./in-proj.txt', 'r') as f:
        line = f.readline()
        line = line[:-1]
        while line != "":
            #print("line = {} \n".format(line))
            line = line[:-1][::-1]
            #print("rev line = {} \n".format(line))
            result_string = result_string + line
            result_string = result_string + "\n"
            line = f.readline()
    print("Here \n{}".format(result_string))
    cs.send(result_string.encode('utf-8'))
    #print("[C]: Data received from server: {}".format(result_string))

    # close the client socket
    cs.close()
    exit()


if __name__ == "__main__":

    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done.")