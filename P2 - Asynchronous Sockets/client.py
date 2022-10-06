import threading
import socket
import sys

def server():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    rs_host = sys.argv[1]
    port = int(sys.argv[2])
    localhost_addr = socket.gethostbyname(rs_host)
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    result_list = []

    with open('./PROJ2-HNS.txt', 'r') as f:
    	for line in f:
    		#print(line)
    		no_space = line.rstrip()
    		actual_line = no_space.lower()
        	cs.send(actual_line.encode('utf-8'))
        	client_data = cs.recv(1000)
        	message_from_client = client_data.decode('utf-8')
        	#print(message_from_client)
        	result_list.append(message_from_client)

    with open('./RESOLVED.txt', 'w') as r:
    	for m in result_list:
            r.write(m)

    cs.close()
    exit()


if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()
