import tempfile
import builtins
from config import load_toml


def test_load_toml(monkeypatch):
    # Создаем временную конфигурацию (кодируем в байтах)
    test_config = b"""
name = "Swoyo_test"
version  = "1.0.0"

[server]
url = "localhost"
timeout = 15
retry_times = 3

[user_data]
username = "name"
password = "admin"
"""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp_file:
        tmp_file.write(test_config)
        tmp_file.flush()
        tmp_filename = tmp_file.name

    # Сохранение оригинальной функции open, чтобы избежать бесконечной рекурсии а setattr
    original_open = builtins.open
    # Подменяем builtins.open, чтобы функция load_toml читала из нашего временного файла
    monkeypatch.setattr("builtins.open", lambda filename, mode: original_open(tmp_filename, mode))

    data = load_toml()
    assert data["name"] == "Swoyo_test"
    assert data["server"]["url"] == "localhost"
    assert data["user_data"]["username"] == "name"
