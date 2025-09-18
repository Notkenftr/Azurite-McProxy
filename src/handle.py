#MIT License

#Copyright (c) 2025 kenftr

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import socket
import threading
from threading import Thread

from src.forward import forward

def handle(client_sock,
           remote_host,
           remote_port,
           buffer):
    """
    Handle a client connection and forward traffic to a remote server.
    :param client_sock: client connection socket
    :param remote_host: target server address.
    :param remote_port: target server port.
    :param buffer: buffer size for forwarding.
    :return:
    """
    try:
        # Create socket to connect to the remote server
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.connect((remote_host,remote_port))

        clientToServer = threading.Thread(target=forward, args=(client_sock, serverSock, buffer, 'C→S'))
        serverToClient = threading.Thread(target=forward, args=(serverSock, client_sock, buffer, 'S→C'))


        clientToServer.start()
        serverToClient.start()


        clientToServer.join()
        serverToClient.join()
    finally:
        try:
            client_sock.close()
        except:
            pass
        try:
            serverSock.close()
        except:
            pass