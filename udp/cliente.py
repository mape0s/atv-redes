import socket 
import threading 

def receber(client_socket):
    while True:
        data, addr = client_socket.recvfrom(1024)
        print(data.decode('utf-8'))

def connect_server(host: str, port: int):
    # cria o socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    nome = input('type your name: ')
    sala = input('type your sala: ')

    client_socket.sendto(f'{nome}!#/entrar {sala}'.encode('utf-8'), (host, port))

    threading.Thread(target=receber, args=(client_socket,), daemon=True).start()

    while True:
        message = input()

        if message[0:4] == '/pv ':
            partes = message.split(' ', 2)   # separa comando, destino e texto
            data = f"{nome}!#/pv {partes[1]} {partes[2]}".encode('utf-8')
            client_socket.sendto(data, (host, port))

        elif message == '/usuarios':
            data = f"{nome}!#/usuarios".encode('utf-8')
            client_socket.sendto(data, (host, port))

        else:
            data = f"{nome}!#{message}".encode('utf-8')
            client_socket.sendto(data, (host, port))

if __name__ == '__main__':
    HOST = 'localhost'   # endereço do servidor
    PORT = 8000          # porta do servidor

    connect_server(HOST, PORT)   # inicia o cliente