import socket


URLS = {
    '/': 'hello index',
    '/blog': 'hello blog'
}


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowen\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 Not fount\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found<\p>'
    if code == 405:
        return '<h1>404</h1><p>Method not allowed<\p>'
    return '<h1>{}</h1>'.format(URLS[url])


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    return (headers + body).encode()


def run():
    # Создаем субъекта(с протоколом IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setsockopt - исполььзуем чтобы установить флаг SO_REUSEADDR в 1
    # позволяет использовать повторно номер порта
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # связываем субъекта с конкретным адресом и портом(адрес, порт)
    server_socket.bind(('localhost', 5000))
    # указываем серверу прослушивать этот адрес и порт
    server_socket.listen()

    # так как общение сервера и клиента может занять неопределенное время.
    # Используем while
    while True:
        # Допустим клиент сделал запрос и мы хотим это посмотреть.
        # Для того чтобы сокет эту информацию получил, используем метод accept
        # Он возвращаяет кортеж(сокет, адрес) - со стороны КЛИЕНТА
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
