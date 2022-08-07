
from socket import *
from sys    import *
from struct import *
import selectors
import os


serverpass = argv[1]
host = argv[2]
port = 5050
serverpass = bytes(serverpass, 'utf-8')
'''
serverpass  = b"password"
host        = "127.0.0.1"
port        = 5005
'''
BUFFER_SIZE = 6144


def recv(conn):
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data:
            break
    conn.send(b't')
    return data


def recieve(key):

    description = key.data
    conn = key.fileobj
    conn.send(b't')
    conn.setblocking(True)

    description = description.decode('utf-8')
    filein = recv(conn)
    key, filename, size = unpack(description, filein)

    if serverpass == key:
        filename = filename.decode("utf-8") + 'a'
        with open(filename, 'wb') as f:
            while size > 0:
                file = conn.recv(BUFFER_SIZE)
                f.write(file)
                size = size - len(file)
            f.close()
        print('finish recieve')
        conn.send(b't')
    conn.setblocking(False)
    sel.unregister(conn)
    conn.close()

def recieve_wrappers(server):
    conn, addr = server.accept()
    print("accept connection from" + addr[0])
    conn.setblocking(False)
    data = conn.recv(BUFFER_SIZE)
    if data:
        print("dataRecieved")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        print("blocking?")
        sel.register(conn, events, data=data)


sel = selectors.DefaultSelector()

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(1)
server.setblocking(False)
sel.register(server, selectors.EVENT_READ, data=None)

try:
    while True:
        event = sel.select(timeout=0.2)
        for key, mask in event:
            print("loopin event")
            if key.data is None:
                recieve_wrappers(server)
                print("continue")
            else:
                print("recieving")
                recieve(key)
except KeyboardInterrupt:
    print("caught Keyboard Interruption")
finally:
    sel.close()









