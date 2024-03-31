import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_host_port():
    # Запрос хоста и порта у пользователя
    host = input("Введите хост (по умолчанию 127.0.0.1): ").strip() or '127.0.0.1'
    while True:
        try:
            port = int(input("Введите порт (по умолчанию 65432): ").strip() or 65432)
            break
        except ValueError:
            print("Порт должен быть целым числом.")
    return host, port

def echo_client():
    # Подключение к серверу
    host, port = get_host_port()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            logger.info(f"Подключено к {host}:{port}")

            while True:
                data = client_socket.recv(1024).decode()
                print(data)  # Выводим сообщение от сервера
                if "Введите ваше имя:" in data:
                    name = input().strip()
                    client_socket.sendall(name.encode())  # Отправляем имя серверу
                else:
                    break  # После отправки имени выходим из цикла ожидания ответа от сервера

            while True:
                user_input = input("Введите сообщение для отправки на сервер (или 'exit' для выхода): ")
                client_socket.sendall(user_input.encode())  # Отправляем сообщение серверу
                if user_input.strip().lower() == "exit":
                    logger.info("Отключение от сервера")
                    break
                data = client_socket.recv(1024)
                print(f"Получен ответ от сервера: {data.decode()}")

        except ConnectionError as e:
            logger.error(f"Ошибка подключения: {e}")
        except Exception as e:
            logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    echo_client()
