import socket

def echo_client():
    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Подключаемся к серверу
    server_address = ('localhost', 8888)
    client_socket.connect(server_address)
    
    try:
        while True:
            # Получаем сообщение для отправки
            message = input("Введите сообщение для отправки серверу (для выхода введите 'exit'): ")
            
            # Отправляем сообщение серверу
            client_socket.sendall(message.encode())
            
            # Проверяем, если пользователь ввел 'exit', то выходим из цикла
            if message.lower() == 'exit':
                break
            
            # Получаем ответ от сервера
            data = client_socket.recv(1024)
            print("Полученный ответ от сервера:", data.decode())
    
    finally:
        # Закрываем соединение с сервером
        client_socket.close()

if __name__ == "__main__":
    echo_client()
