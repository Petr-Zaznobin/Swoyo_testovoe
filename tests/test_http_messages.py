import json
from http_messages import HttpRequest, HttpResponse


def test_http_request_to_from_bytes():
    headers = {
        "Host": "localhost",
        "Content-Type": "application/json",
        "Content-Length": "27"
    }
    body = json.dumps({
        "sender": "111",
        "recipient": "222",
        "message": "Hello"
    })
    print(body)
    request = HttpRequest(path="/send_sms", headers=headers, body=body)
    bytes_data = request.to_bytes()
    request_parsed = HttpRequest.from_bytes(bytes_data)

    assert request.method == request_parsed.method
    assert request.path == request_parsed.path
    assert request.headers == request_parsed.headers
    assert request.body == request_parsed.body


def test_http_response_to_from_bytes():
    headers = {"Content-Type": "application/json"}
    body = '{"status": "success"}'
    response = HttpResponse(status_code=200, headers=headers, body=body)
    bytes_data = response.to_bytes()
    response_parsed = HttpResponse.from_bytes(bytes_data)

    assert response.status_code == response_parsed.status_code
    assert response.headers == response_parsed.headers
    assert response.body == response_parsed.body
