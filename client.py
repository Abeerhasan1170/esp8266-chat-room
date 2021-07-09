import socket
import select
import errno
import sys
class Color:
    Black="\033[30m"
    Red="\033[31m"
    Green="\033[32m"
    Yellow="\033[33m"
    Blue="\033[34m"
    Magenta="\033[35m"
    Cyan="\033[36m"
    White="\033[37m"
    Reset="\033[0m"
c = Color()

HEADER_LENGTH = 10
IP = "192.168.1.104"
PORT = 1234
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
while True:
    readers, _, _ = select.select([sys.stdin, client_socket],[],[])
    for reader in readers:
        if reader == client_socket:
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()
                    username_length = int(username_header.decode('utf-8').strip())
                    username = client_socket.recv(username_length).decode('utf-8')
                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')
                    print('%s%s%s > %s' % (c.Red,username,c.Reset,message))

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
        else:
            message = sys.stdin.readline().strip()
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
#
#        # We just did not receive anything
#        continue
#
#    except Exception as e:
#        # Any other exception - something happened, exit
#        print('Reading error: '.format(str(e)))
#        sys.exit()
