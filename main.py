import socket
import select

HEADER_LENGTH = 10

IP = "192.168.1.104"
PORT = 1234
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(3)
sockets_list = [server_socket]
clients = []
print('Listening for connections on %s:%d' % (IP,PORT))

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients.append(user)
            print('Accepted new connection from {}:{}, username: {}'.format(client_address[0],client_address[1], user['data'].decode('utf-8')))
        else:
            message = receive_message(notified_socket)
            if message is False:
                idx = sockets_list.index(notified_socket) - 1
                print('Closed connection from: {}'.format(clients[idx]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[idx]
                continue
            idx = sockets_list.index(notified_socket) - 1
            user = clients[idx]
            print('Received message from %s: %s' % (user["data"].decode("utf-8"), message["data"].decode("utf-8")))
            for client_socket in sockets_list[1:]:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        
        sockets_list.remove(notified_socket)
        clients.remove(notified_socket)

