import threading
import socket
import sys
import signal
import time

#def signal_handler(sig, frame):
#    sys.exit(0)

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    dns_ip = {}
    dns_type = {}

    with open('./PROJ2-DNSTS1.txt', 'r') as f:
    	for line in f:
         	split_line = line.split(" ")
         	lower_key = split_line[0].lower()
            	dns_ip[lower_key.encode('utf-8')] = split_line[1]
            	dns_type[lower_key.encode('utf-8')] = split_line[2]
    port_num = int(sys.argv[1])
    server_binding = ('',  port_num)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    try:
    	print("[S]: Server IP address is {}".format(localhost_ip))
    	csockid, addr = ss.accept()
    	print("[S]: Got a connection request from a client at {}".format(addr))
    	#does bind and request, loads dictionary from file, looks at query, sends response or no response
    	#put receiving logic in a loop
    	counter = 1
    	while counter == 1:
    		if csockid.fileno() == -1:
    			sys.exit(0)
         	raw_query = csockid.recv(1000)
         	if raw_query:
         		query = str(raw_query)
         		#print("Query is " + query)
         		for key in dns_ip:
         			#print("Key is " + key)
         			#print(type(key))
         			#print(type(query))
         			#print(len(key))
         			#print(len(query))
         			if key == query:
         				result_string = query + " " + dns_ip[key] + " " + dns_type[key] + " IN"
            				#print("Result is " + result_string)
            				csockid.send(result_string.encode('utf-8'))
            			
            	else:
            		print("Error, nothing from socket")
			sys.exit(0)
    except KeyboardInterrupt:
    	sys.exit(0)

    ss.close()
    exit()


if __name__ == "__main__":
    t2 = threading.Thread(name='server', target=server)
    t2.start()
    
    #signal.signal(signal.SIGINT, signal_handler)

