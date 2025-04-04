# Swoyo_testovoe

## Тестовое задание на позицию Python стажёра
**Простой CLI-клиент для отправки СМС-сообщений через HTTP-сервис**

## Описание проекта

Данный проект реализует клиент, который:
- Загружает настройки из файла конфигурации в формате TOML.
- Принимает через командную строку параметры: номер отправителя, номер получателя и текст СМС.
- Формирует HTTP-запрос в соответствии со спецификацией сервиса (с авторизацией Basic Auth).
- Отправляет запрос через TCP-сокет и выводит полученный HTTP-код и тело ответа.
- Логирует переданные параметры и ответы от сервиса в лог-файл (настройки логирования задаются в конфигурационном файле).


## Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Petr-Zaznobin/Swoyo_testovoe.git
   cd Swoyo_testovoe
   
2. **Для редактирования и запуска тестов установите pytest**
   ```bash
   pip install pytest

3. **Отредактируйте данные в TOML**
   
   Измените поля в config.toml, если имеется необходимость

4. **Скачайте Prism для своей платформы**
   
   Windows / Linux / macOS: [репозиторий prism](https://github.com/stoplightio/prism/releases)

5. **Запустите мок-сервер**
  * Linux:
    ```bash
    ./prism-cli-linux mock sms-platform.yaml
    
  * macOS: 
    ```bash
    ./prism-cli-macos mock sms-platform.yaml
    
  * Windows:
    ```bash
    ./prism-cli-win.exe mock sms-platform.yaml

6. **Создайте новое терминал-окно**
* macOS / Linux:
   ```bash
   python3 main.py --num_send "111111111" --num_receive "222222222" --text "example"

* Windows:
   ```bash
   python main.py --num_send "111111111" --num_receive "222222222" --text "example"

7. **В случае ошибок**
   
   Проверьте логи в app.log



---------
## Заключение
Проект создан для компании Swoyo в качестве тестового задния на позицию Python-разработчик

Проект создан согласно заданию из файла *Тестовое задание. Стажёр в Python.pdf*
