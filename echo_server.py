# echo_server.py

import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000) # host, port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) 
    # Fix port is used issue
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # bind your sock to the address and begin to listen for incoming connections
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)
            # make new socket when client connects and get client address
            conn, addr = sock.accept()
            
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # receive 16 bytes of data from client
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))
                    # send the data received back to the client, log using print statement 
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))
                    # check if recieved msg, if recieved msg then break the while loop 
                    if len(data) < 16:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

            finally:
                # close the socket you created above when a client connected
                print('echo complete, client connection closed', file=log_buffer)
                conn.close()

    except KeyboardInterrupt:
        # close the server socket and exit from the server function
        sock.close() # double check****
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
