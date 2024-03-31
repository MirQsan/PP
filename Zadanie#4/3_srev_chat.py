import socket
import threading

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8888))
        self.server_socket.listen(5)
        self.clients = {}
        self.messages = []

    def broadcast(self, message, sender):
        for client_socket, username in self.clients.values():
            if client_socket != sender:
                try:
                    client_socket.send(message.encode())
                except:
                    client_socket.close()
                    del self.clients[client_socket]
                    print(f"Потеряно соединение с {username}")
                    break

    def handle_client(self, client_socket, username):
        self.clients[client_socket] = (username,)

        # Отправляем историю сообщений новому клиенту
        for message in self.messages:
            client_socket.send(message.encode())

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"{username}: {message}")
                    self.messages.append(f"{username}: {message}")
                    self.broadcast(f"{username}: {message}", client_socket)
                else:
                    raise Exception()
            except:
                client_socket.close()
                del self.clients[client_socket]
                print(f"{username} покинул чат")
                break

    def start(self):
        print("Сервер запущен. Ожидание подключений...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            username = client_socket.recv(1024).decode()
            print(f"Подключен пользователь: {username}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, username))
            client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
