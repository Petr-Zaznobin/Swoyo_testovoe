import socket
from main import main


# Фиктивный сокет для эмуляции отправки/получения данных
class DummySocket:
    def __init__(self, *args, **kwargs):
        self.sent_data = b"" # данные, отправляемые через сокет
        self.responses = [b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSuccess"] # список байтовых строк, которые будут возвращены при вызове метода "recv"
        self.current_chunk = 0 # индекс текущего ответа для последовательного чтения

    def settimeout(self, timeout):
        self.timeout = timeout

    def connect(self, address):
        self.address = address

    def sendall(self, data):
        self.sent_data += data

    def recv(self, bufsize):
        if self.current_chunk < len(self.responses):
            chunk = self.responses[self.current_chunk]
            self.current_chunk += 1
            return chunk
        return b""

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def dummy_socket(*args, **kwargs):
    return DummySocket()


# Данные для конфигурации и аргументов CLI
class DummyArgs:
    num_send = "111"
    num_receive = "222"
    text = "Test message"


def dummy_load_toml():
    return {
        "server": {"url": "http://localhost:4010", "timeout": 5},
        "user_data": {"username": "Peter", "password": "admin"}
    }


def dummy_parse_cli_args():
    return DummyArgs()


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("main.load_toml", dummy_load_toml)
    monkeypatch.setattr("main.parse_cli_args", dummy_parse_cli_args)
    monkeypatch.setattr(socket, "socket", dummy_socket)

    main()
    captured = capsys.readouterr().out # возвращает содержимое стандартного вывода в консоль от main()

    assert "HTTP код: 200" in captured
    assert "Тело ответа: Success" in captured
