import socket

# socket.socket(
#   AF_INET - будет использоваться "имя хоста и номер порта",
#   socket.SOCK_STREAM - будет использоваться протокол TCP
# )
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# setsockopt - исполььзуем чтобы установить флаг SO_REUSEADDR в 1
#    позволяет использовать повторно номер порта
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
# прослушиваем запросы от клиентов которые хотят подключится
server_socket.listen()

connections = []

try:
    while True:
        # ждем запрос на подключение
        connection, client_address = server_socket.accept()
        print(f'Получен запрос на подключение от {client_address}!')
        connections.append(connection)

        for connection in connections:
            buffer = b''
            # \r\n - в telnet эта пара добавляется в конец строки при нажатии Enter
            # while buffer[-2:] != b'\r\n':
            while True:
                # метод recv() позволяет получать данные из сокета
                # 2 - количество байтов которые мы хотим получить
                data = connection.recv(4096)
                if not data:
                    break
                else:
                    print(f'Получены данные: {data}!')
                    buffer = buffer + data
            print(f'Все данные: {buffer}')
            # sendall принимает сообщение и отправляет его клиенту
            connection.send(buffer)
finally:
    server_socket.close()
