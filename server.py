# import sys for exit
import sys

# import argument parsing library
import argparse

# import libraries for logging
from datetime import datetime

# import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

# Logging
def log(level):
    time = datetime.now().isoformat()
    return lambda message: print(f'[{time} {level}] {message}')

INFO = log('\x1b[32mINFO\x1b[0m')
WARN = log('\x1b[33mWARN\x1b[0m')
ERROR = log('\x1b[31mERROR\x1b[0m')

# create a parser for arguments
parser = argparse.ArgumentParser()

# if you run python server.py -p 3000 the server will run on port 3000, or else
# the server will run on port 8090 by default, you can also use --port or type
# help to see more information
# run `python server.py --help` for more information
port_help = 'run server using a specific port'
parser.add_argument('-p', '--port', type=int, default=8090, help=port_help)

args = parser.parse_args()

# The server binds to your COMPUTERS internal ip address, which gets forwarded
# to the home or private ip address that is bound to your computer.
# e.g. if your private ip is 192.168.1.11 then access the server on
# 192.168.1.11:8090 which is forwarded from 127.0.0.1:8090
serverName = '127.0.0.1'
serverPort = args.port

serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
INFO(f'Running server at: http://{serverName}:{serverPort}')

while True:
    # Establish the connection
    INFO('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(4096)
        INFO(message.decode())

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # HTTP OK Status
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
        
        # HTTP Headers
        connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
        connectionSocket.send('Server: server.py\r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        # Send the content of the requested file to the client
        for item in outputdata:
            connectionSocket.send(item.encode())
        
        connectionSocket.send('\r\n'.encode())
        connectionSocket.close()

    except IOError:
        # Log Error
        ERROR('404: Could not find specified path')

        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 NOT FOUND\r\n'.encode())
        connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        
        not_found = open('www/404.html').read()
        for item in not_found:
            connectionSocket.send(item.encode())

        connectionSocket.send('\r\n'.encode())
        
        # Close client socket
        connectionSocket.close()

       
    # Terminate the program after sending the corresponding data
    serverSocket.close()
    sys.exit()
