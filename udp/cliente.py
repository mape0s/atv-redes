import socket          # biblioteca para comunicação em rede
import threading       # biblioteca para criar threads

# função que fica recebendo mensagens do servidor
def receber(client_socket):
    while True:   # loop infinito
        data, addr = client_socket.recvfrom(1024)   # recebe até 1024 bytes
        print(data.decode('utf-8'))   # converte bytes em texto e mostra

# função principal do cliente
def connect_server(host: str, port: int):
    # cria o socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # pede nome e sala
    nome = input('type your name: ')
    sala = input('type your sala: ')

    # envia comando para entrar na sala
    client_socket.sendto(f'{nome}!#/entrar {sala}'.encode('utf-8'), (host, port))

    # cria thread para receber mensagens enquanto o usuário digita
    threading.Thread(target=receber, args=(client_socket,), daemon=True).start()

    # loop principal para enviar mensagens
    while True:
        message = input()

        # se for mensagem privada
        if message[0:4] == '/pv ':
            partes = message.split(' ', 2)   # separa comando, destino e texto
            data = f"{nome}!#/pv {partes[1]} {partes[2]}".encode('utf-8')
            client_socket.sendto(data, (host, port))

        # se pedir lista de usuários
        elif message == '/usuarios':
            data = f"{nome}!#/usuarios".encode('utf-8')
            client_socket.sendto(data, (host, port))

        # mensagem normal para a sala
        else:
            data = f"{nome}!#{message}".encode('utf-8')
            client_socket.sendto(data, (host, port))

# ponto inicial do programa
if __name__ == '__main__':
    HOST = 'localhost'   # endereço do servidor
    PORT = 8000          # porta do servidor

    connect_server(HOST, PORT)   # inicia o cliente