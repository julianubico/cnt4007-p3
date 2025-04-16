import threading
import sys
import socket

if (len(sys.argv) != 2):
    raise Exception("python chat.py <port>")

PORT = sys.argv[1]
if not PORT.isdigit():
    raise Exception("Port must be a number")
PORT = int(PORT)

def read_from_socket(sock: socket):
    while True:
        client, address = sock.accept()
        print(f"Connected to {address}")
        try:
            while True:
                data = client.recv(1024)
                if not data: break
                print(data.decode())
        finally: client.close()
def write_to_socket(sock: socket):
    try:
        while True:
            message = input()
            sock.sendall(message.encode())
    finally: sock.close()

read_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
read_socket.bind(('localhost', PORT))
read_socket.listen(1)
print(f"Listening on port {PORT}...")
reading_thread = threading.Thread(target=read_from_socket, args=(read_socket,))
reading_thread.start()

CHANNEL = input("Enter port to connect to: ")
if not CHANNEL.isdigit():
    raise Exception("Port must be a number")
CHANNEL = int(CHANNEL)

write_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
write_socket.connect(('localhost', CHANNEL))  
print(f"Connected to {CHANNEL}")
writing_thread = threading.Thread(target=write_to_socket, args=(write_socket,))
writing_thread.start()

reading_thread.join()
writing_thread.join()