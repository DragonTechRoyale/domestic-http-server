# Written by Ed Lustig
import socket
import os


HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
AADR = (SERVER, PORT)
FORMAT = 'utf-8'


HTTP_OK = "HTTP/1.1 200 OK\r\n"
ACC = "\r\nAccept:text/html\r\n"
CONTENT_LENGTH = "\r\nContent-Length:"
CONTENT_HTML = "Content-Type: text/html; charset=utf-8"
CONTENT_GIF = "Content-Type: image/gif"
HTTP_ERROR = "HTTP/1.1 404\r\n"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(AADR)
    server_socket.listen(1)
    print(f"listening on port {PORT}")

    while True:
        client_connection, client_address = server_socket.accept()  # Wait for client connections

        while True:
            request = client_connection.recv(1024).decode()  # Get the client request
            print(request)

            request_empty = request == "" 
            if request_empty:
                print("the request isn't a valid HTTP request")
                response = """HTTP/1.0 200 OK\n\n
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <title>cyber</title>
                            </head>
                            <body>
                            <h1>500 internal server error</h1>
                            </body>
                            </html>"""
                print(f"500, response: \"{response}\"")
                client_connection.send(response.encode())

            lines = request.split('\n')
            line = lines[0].split(' ')
            file_name = line[1]

            if file_name == "/dome_kano.jpg":
                response = f"""HTTP/1.0 200 OK\n\n
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>cyber</title>
                    </head>
                    <body>
                    <h1>302 Moved Temporary, try "000-1.jpg" instead</h1>
                    </body>
                    </html>"""
                print(f"302, response: \"{response}\"")
                client_connection.send(response.encode())
            elif os.path.isfile(f"files/{file_name}"):
                file_name = file_name.replace('/', '')
                file_type = file_name.split('.')[1]
                if file_type == "jpg" or file_type == "png":
                    if file_name == "bt_color_v01_001.png":
                        # 403 forbidden
                        response = f"""HTTP/1.0 200 OK\n\n
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <title>cyber</title>
                            </head>
                            <body>
                            <h1>403 forbidden</h1>
                            </body>
                            </html>"""
                        print(f"403, response: \"{response}\"")
                        client_connection.send(response.encode())
                    else:
                        file = open(f"files/{file_name}", "rb")
                        file_binary = file.read()
                        file.close()
                        header = HTTP_OK + f"Content-Type: image/{file_type}" + CONTENT_LENGTH + str(len(file_binary)) + ACC + "\r\n"
                        print(f"image, sending {file_name}")
                        client_connection.send(header.encode() + file_binary)
                elif file_type == "txt" or "html" or "py" or "c" or "asm":
                    client_connection.send(response.encode())
                    file = open(f"files/{file_name}", "rb")
                    text = file.read()
                    file.close()
                    response = f"""HTTP/1.0 200 OK\n\n
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <title>cyber</title>
                            </head>
                            <body>
                            <h1>{text}</h1>
                            </body>
                            </html>"""
                    print(f"text file, response: \"{response}\"")
                    client_connection.send(response.encode())
                else:
                    # return 404_page.html
                    response = """HTTP/1.0 200 OK\n\n
                                <html lang="en">
                                <head>
                                <meta charset="UTF-8">
                                <title>cyber</title>
                                </head>
                                <body>
                                <h1>404 file not found</h1>
                                </body>
                                </html>"""
                    print(f"404, response: \"{response}\"")
                    client_connection.send(response.encode())
            elif file_name == '/' or file_name == "/index.html":
                # return index.html
                response = """HTTP/1.0 200 OK\n\n
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <title>cyber</title>
                            </head>
                            <body>
                            <h1>Welcome to the image site, add file name go the URL to view it if it exists</h1>
                            </body>
                            </html>"""
                print(f"got \"/\", response: \"{response}\"")
                client_connection.send(response.encode())
            else:
                # return 404_page.html
                response = """HTTP/1.0 200 OK\n\n
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <title>cyber</title>
                            </head>
                            <body>
                            <h1>404 file not found</h1>
                            </body>
                            </html>"""
                print(f"404, response: \"{response}\"")
                client_connection.send(response.encode())

            client_connection.close()
            break

    server_socket.close()


if __name__ == '__main__':
    main()
