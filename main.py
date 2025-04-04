import socket
import json
import base64
from argparse import Namespace

from config import load_toml
from cli import main as parse_cli_args
from http_messages import HttpRequest, HttpResponse

import logging


def extract_host_port(url: str):
    url = url[len("http://"):]
    host, port_str = url.split(":", 1)
    port = int(port_str)

    return host, port


def build_request(args: Namespace, config: dict[str, any]) -> HttpRequest:
    request_body = json.dumps({
        "sender": args.num_send,
        "recipient": args.num_receive,
        "message": args.text
    })
    server_url = config["server"]["url"]
    host, _ = extract_host_port(server_url)
    headers = {
        "Host": host,
        "Content-Type": "application/json",
        "Content-Length": str(len(request_body))
    }
    username = config["user_data"]["username"]
    password = config["user_data"]["password"]
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers["Authorization"] = f"Basic {encoded_credentials}"

    # Новый путь запроса "/send_sms"
    path = "/send_sms"
    #print(headers, request_body)
    return HttpRequest(path=path, headers=headers, body=request_body)


def send_request(request: HttpRequest, host: str, port: int, timeout: int) -> bytes:
    request_bytes = request.to_bytes()
    response_bytes = b""
    # Создание TCP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(request_bytes)
        # Принимаем ответ
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            response_bytes += chunk
    return response_bytes

def setup_logging(config: dict[str, any]):
    # Извлекаем параметры логирования из конфигурации
    log_level_str = config.get("logging", {}).get("level", "INFO")
    log_file = config.get("logging", {}).get("file", "app.log")
    # Преобразуем уровень логирования в число
    numeric_level = getattr(logging, log_level_str.upper(), logging.INFO)
    # Настраиваем логирование
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=log_file,
        filemode="a"
    )
    logging.info("Логирование запущено. Уровень: %s, Файл: %s", log_level_str, log_file)


def main():
    config = load_toml()

    setup_logging(config)

    args = parse_cli_args()
    logging.info("Получены аргументы командной строки: %s", args)

    request = build_request(args, config)
    host, port = extract_host_port(config["server"]["url"])
    timeout = config["server"].get("timeout", 15)
    response_bytes = send_request(request, host, port, timeout)
    response = HttpResponse.from_bytes(response_bytes)
    logging.info("Получен ответ от сервиса: HTTP код %s, тело: %s", response.status_code, response.body)
    #print(request)
    print("HTTP код:", response.status_code)
    print("Тело ответа:", response.body)


if __name__ == "__main__":
    main()
