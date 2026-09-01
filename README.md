# grpc-sketch

Пример gRPC-клиента и сервера.

## Требования

- Windows
- Python 3.11
- Cmake >= 3.13
- OpenSSL

## Порядок запуска

Из корня репозитория:

1. `create_venv.bat` — создать виртуальное окружение Python 3.11
2. `install_packages.bat` — установить pip-зависимости
3. `build.bat` — сгенерировать код для gRPC
4. `start_server.bat` — запустить API (`http://localhost/api/1.0`, debugpy на порту 5678)
5. `start_cient.bat` — запустить клиентский пример
