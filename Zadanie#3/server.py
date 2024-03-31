import socket
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_host_port():
    host = input("Введите хост (по умолчанию 127.0.0.1): ").strip() or '127.0.0.1'
    port = input("Введите порт (по умолчанию 65432): ").strip() or 65432
    return host, int(port)

def setup_logging():
    logging.basicConfig(filename='server_log.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def find_available_port(host, start_port):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
                temp_socket.bind((host, port))
            return port
        except OSError:
            port += 1

def load_known_clients():
    try:
        with open("known_clients.txt", "r") as f:
            known_clients = {line.strip().split(":")[0]: line.strip().split(":")[1] for line in f.readlines()}
    except FileNotFoundError:
        known_clients = {}
    return known_clients

def save_known_client(ip_address, client_name):
    with open("known_clients.txt", "a") as f:
        f.write(f"{ip_address}:{client_name}\n")

def handle_client(conn, addr):
    logger.info(f"Подключился клиент {addr}")
    known_clients = load_known_clients()

    if addr[0] in known_clients:
        client_name = known_clients[addr[0]]
        conn.sendall(f"Добро пожаловать, {client_name}!\n".encode())
    else:
        conn.sendall("Введите ваше имя:\n".encode())
        client_name = conn.recv(1024).decode().strip()
        save_known_client(addr[0], client_name)
        conn.sendall(f"Добро пожаловать, {client_name}!\n".encode())

    # Создаем файл для записи сообщений от клиента
    client_log_filename = f"{client_name}_{addr[0]}.txt"
    with open(client_log_filename, "a") as client_log_file:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    logger.info("Клиент отключился")
                    break
                message = data.decode()
                logger.info(f"Получено от {client_name}: {message}")
                if message.strip().lower() == "exit":
                    logger.info("Клиент запросил отключение")
                    break
                conn.sendall(data)
                client_log_file.write(message + '\n')
            except Exception as e:
                logger.error(f"Ошибка при обработке запроса от клиента {addr}: {e}")
                break
    conn.close()

def echo_server():
    setup_logging()
    host, port = get_host_port()
    port = find_available_port(host, port)
    logger.info(f"Сервер запущен на {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    echo_server()
