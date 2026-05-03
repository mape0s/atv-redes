import socket

usuarios = {}
salas = {}

# Função de log:
# Mostra no terminal e salva no arquivo log.txt
def log(msg):
    print(msg)
    open('log.txt', 'a').write(msg + '\n')

# Função de envio geral (broadcast):
# Envia uma mensagem para todos os usuários de uma mesma sala
def enviar(server_socket, msg, sala):
    for name in salas:
        if salas[name] == sala:
            server_socket.sendto(msg.encode('utf-8'), usuarios[name])

# Função principal do servidor:
# Responsável por receber interpretar e encaminhar mensagens
def start_server(host, port):

    # Cria o servidor UDP e inicia na porta definida
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    log('server started')

    # Loop principal: fica escutando mensagens dos clientes
    while True:
        data, addr = server_socket.recvfrom(1024)

        # Protocolo usado: "nome!#mensagem"
        # Aqui separa quem enviou e o conteúdo
        name = data.decode('utf-8').split('!#')[0]
        message = data.decode('utf-8').split('!#')[1]

        # 1. Entrar na sala
        if message[0:8] == '/entrar ':
            sala = message.split(' ')[1]

            # salva usuário e sala
            usuarios[name] = addr
            salas[name] = sala

            log(name + ' entrou em ' + sala)

            # avisa todos da sala
            enviar(server_socket, name + ' entrou', sala)

        # 2. Listar usuários
        elif message == '/usuarios':
            lista = ', '.join(usuarios.keys())
            server_socket.sendto(lista.encode('utf-8'), addr)

        # 3. Mensagem privada
        elif message[0:4] == '/pv ':
            partes = message.split(' ', 2)
            dest = partes[1]
            texto = partes[2]

            log(name + ' -> ' + dest + ': ' + texto)

            # envia para o destinatário
            server_socket.sendto(
                ('[pv de ' + name + ']: ' + texto).encode('utf-8'),
                usuarios[dest]
            )

        # 4. Mensagem normal para a sala
        else:
            log(name + ': ' + message)

            # envia para todos da mesma sala
            enviar(server_socket, name + ': ' + message, salas[name])

# Inicia o servidor
if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8000
    start_server(HOST, PORT)