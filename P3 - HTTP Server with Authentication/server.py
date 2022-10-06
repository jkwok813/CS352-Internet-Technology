import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    #print "Here is the", tag
    #print "\"\"\""
    #print value
    #print "\"\"\""
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users

f = open ("secrets.txt", "r")
Line = f.readline()
secrets = {}
key = 0
secretslist = []
while Line != "":
    secrets[key] = Line
    key+=1
    secretslist.append(Line)
    Line = f.readline()
#print(secrets) 

f = open ("passwords.txt", "r")
Line = f.readline()
passwords = {}
key = 0
passlist = []
while Line != "":
    passwords[key] = Line
    key+=1
    passlist.append(Line)
    Line = f.readline()
#print(passwords) 

firstsearch = True
secondsearch = False
cookiejar = {}

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    
    username = ""
    password = ""
    logout = False
    empty = False
    login = False
    if(body == ""):
        #print("help")
        empty = True
    if(body != ""):
        if(body == "action=logout"):
            html_content_to_send = logout_page
            logout = True
        else:
            x = body.split("&")
            #print(x)
            username = x[0].replace("username=", "") 
            password = x[1].replace("password=", "")
            print('username is ' + username + ', password is ' + password)
    
    # You need to set the variables:
    # (1) `html_content_to_send` => add the HTML content you'd
    # like to send to the client.
    # Right now, we just send the default login page.
    html_content_to_send = login_page
    dlength = len(passwords)
    x = 0
    secr = ""
    login_success = False
    for z in passlist:
        #print(x)
        x = z.split()
        if username == x[0] and password == x[1]:
            login_success = True
            break
    if login_success == True:
        for w in secretslist:
            y = w.split()
            if username == y[0]:
                secr = y[1]
                html_content_to_send = success_page + secr
                rand_val = random.getrandbits(64)
                headers_to_send = 'Set-Cookie: token=' + str(rand_val) + '\r\n'
                cookiejar[str(rand_val)] = username
                login = True
                firstsearch = False
                print(str(rand_val))
                break
    else:
        #print("body is " + body)
        html_content_to_send = bad_creds_page     
    if(empty == True):
        print("empty is true")
        html_content_to_send = login_page
    if(secondsearch == True):
        #check cookie
        headercookie = ""
        result = headers.find('token=')
        if(result != -1):
            headercookie = headers[result+6:]
        if cookiejar.has_key(headercookie):
            print("Valid cookie")
            un = cookiejar[headercookie] 
            for w in secretslist:
                y = w.split()
                if un == y[0]:
                    secr = y[1]
                    html_content_to_send = success_page + secr
                    break
        else:
            print("Invalid cookie")
            print(cookiejar)
            print(headercookie)
            html_content_to_send = bad_creds_page
    if(logout == True):
        html_content_to_send = logout_page                      
    #html_content_to_send = login_page
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page
    
    # (2) `headers_to_send` => add any additional headers
    # you'd like to send the client?
    # Right now, we don't send any extra headers.
    if(login == False):
        headers_to_send = ''
    if firstsearch == False:
        secondsearch = True
    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print "Served one request/connection!"
    print

# We will never actually get here.
# Close the listening socket
sock.close()
