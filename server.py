
from socket import *
from sys    import *
from struct import *
import os


serverpass = argv[1]
host = '45.76.124.45'
port = 22

'''
serverpass  = b"password"
host        = "127.0.0.1"
port        = 5005
'''
BUFFER_SIZE = 6144


def recv(con):
    while 1:
        data = con.recv(BUFFER_SIZE)
        if data:
            break
    conn.send(b't')
    return data


def recieve(conn):
    description = recv(conn)
    description = description.decode('utf-8')
    filein = recv(conn)
    key, filename, size = unpack(description, filein)
    print(size)
    print(key)
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
    conn.close()


server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(1)
conn, addr = server.accept()
print('connected to', addr)
recieve(conn)




