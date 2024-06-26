import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())
        if message.lower() == "exit":
            client_socket.close()
            break

def chat_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    username = input("Введите ваше имя: ")
    client_socket.send(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    send_thread.join()

if __name__ == "__main__":
    chat_client()
