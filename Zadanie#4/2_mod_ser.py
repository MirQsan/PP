import socket
import threading

def handle_client(client_socket):
    while True:
        # Принимаем данные от клиента
        data = client_socket.recv(1024)
        if not data:
            break
        
        # Отправляем данные обратно клиенту
        client_socket.send(data)
    
    # Закрываем соединение с клиентом
    client_socket.close()

def echo_server():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Привязываем сокет к адресу и порту
    server_socket.bind(('localhost', 8888))
    
    # Слушаем входящие подключения
    server_socket.listen(5)
    
    print("Сервер запущен. Ожидание подключений...")
    
    while True:
        # Принимаем входящее подключение
        client_socket, addr = server_socket.accept()
        print(f"Подключение установлено с {addr[0]}:{addr[1]}")
        
        # Создаем новый поток для обработки подключения
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    echo_server()
