class HttpRequest():
    method: str
    path: str
    headers: dict
    body: str
    def __init__(self, path: str, headers: dict, body: str, method: str = 'POST'):
        self.method = method # метод запроса
        self.path = path # URL-путь
        self.headers = headers # заголовки запроса
        self.body = body # тело запроса

    def to_bytes(self) -> bytes:
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers_str = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        return (request_line + headers_str + "\r\n" + self.body).encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HttpRequest":
        text = binary_data.decode("utf-8")
        lines = text.split("\r\n")
        request_line = lines[0]
        parts = request_line.split(" ")
        method = parts[0]
        path = parts[1]
        headers = {}
        i = 1
        while i < len(lines) and lines[i] != "":
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()
            i += 1
        body = "\r\n".join(lines[i+1:]) if i+1 < len(lines) else ""
        return cls(path=path, headers=headers, body=body, method=method)

class HttpResponse():
    status_code: int # код ответа
    headers: dict # заголовки ответа
    body: str # содержимое ответа
    def __init__(self, status_code: int, headers: dict, body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        status_text = {
            200: "OK",
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error"
        }.get(self.status_code, "")
        status_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n" #"{HTTP-версия} {код состояния} {текст состояния}\r\n"
        headers_str = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        return (status_line + headers_str + "\r\n" + self.body).encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HttpResponse":
        text = binary_data.decode("utf-8")
        lines = text.split("\r\n")
        status_line = lines[0]
        parts = status_line.split(" ", 2)
        status_code = int(parts[1])
        headers = {}
        i = 1
        while i < len(lines) and lines[i] != "":
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()
            i += 1
        body = "\r\n".join(lines[i+1:]) if i+1 < len(lines) else ""
        return cls(status_code=status_code, headers=headers, body=body)
