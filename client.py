
from socket import *
from struct import *
from sys    import *
import os


file = argv[1]
key = argv[2]
host = argv[3]
port = 5050
address = (host, port)


'''
file = "luv.mp3"
key = "password"
host = "127.0.0.1"
port = 5005
address = (host, port)
'''

BUFFER_SIZE = 6144
print(file)
size = os.path.getsize(file)


filename = bytes(file, 'utf-8')
key = bytes(key, 'utf-8')


def slength(ob):
    return str(len(ob) + 1) + 'p'


def describe(key, filename, size):
    description = slength(key) + slength(filename) + 'i'
    return description


def recv(con):
    while 1:
        data = con.recv(BUFFER_SIZE)
        if data:
            break
    print(data)
    return data


def send_description(skt, description):
    print("begin send des")
    description = bytes(description, 'utf-8')
    skt.send(description)
    return bool(recv(skt))


def send_info(skt:object, description) -> object:
    package = pack(description, key, filename, size)
    skt.send(package)
    return bool(recv(skt))


def send_file(skt: object) -> object:
    with open(file, 'rb') as f:
        for data in f:
            skt.send(data)
            print(len(data))
        f.close()
    return bool(recv(skt))


'require try...except'


def send(skt:object) -> object:
    print("begin send")
    desciption = describe(key, filename, size)
    if send_description(skt, desciption) and send_info(skt, desciption):
        if send_file(skt):
            print('done')
            skt.close()
        else:
            print('file_send_error')
    else:
        print("info_send_error")


client = socket(AF_INET, SOCK_STREAM)
client.connect(address)
send(client)



