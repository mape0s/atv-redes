import socket
 
usuarios = {}
salas = {}
 
def log(msg):
    print(msg)
    open('log.txt', 'a').write(msg + '\n')
 
def broadcast(server_socket, msg, sala):
    for name in salas:
        if salas[name] == sala:
            server_socket.sendto(msg.encode('utf-8'), usuarios[name])
 
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    log('server started')
 
    while True:
        data, addr = server_socket.recvfrom(1024)
        name = data.decode('utf-8').split('!#')[0]
        message = data.decode('utf-8').split('!#')[1]
 
        if message[0:8] == '/entrar ':
            sala = message.split(' ')[1]
            usuarios[name] = addr
            salas[name] = sala
            log(name + ' entrou em ' + sala)
            broadcast(server_socket, name + ' entrou', sala)
 
        elif message == '/usuarios':
            lista = ', '.join(usuarios.keys())
            server_socket.sendto(lista.encode('utf-8'), addr)
 
        elif message[0:4] == '/pv ':
            partes = message.split(' ', 2)
            dest = partes[1]
            texto = partes[2]
            log(name + ' -> ' + dest + ': ' + texto)
            server_socket.sendto(('[pv de ' + name + ']: ' + texto).encode('utf-8'), usuarios[dest])
 
        else:
            log(name + ': ' + message)
            broadcast(server_socket, name + ': ' + message, salas[name])
 
if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8000
    start_server(HOST, PORT)