import socket

PORT = 8080
IP = '127.0.0.1'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(( IP, PORT ))
server.listen(1)

try:
    while True:
        socketCliente, addressCliente = server.accept()
        print(f"Conexão com {addressCliente[0]}:{socketCliente}")
        socketCliente.close()
except KeyboardInterrupt:
    print('Encerrando...')
finally:
    server.close()