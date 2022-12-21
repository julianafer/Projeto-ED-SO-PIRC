import socket
from style import style
import globals

HOST = 'localhost'
PORT = 1500

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
globals.servidor = (HOST, PORT)

print("\n--- Bem-vindo ao Say Hello! ---\n")

def join():
    entrada = input()
    cliente.sendall(entrada.encode())
    msg_server, globals.servidor = cliente.recvfrom(2048)
    print(msg_server.decode())

def connect():
    try:
        cliente.connect(globals.servidor)
        print(f'{style.GREEN}• Conectado\n{style.RESET}')
    except:
        print(f'{style.RED}• Não foi possível conectar-se{style.RESET}\n')
        return False
    username = 'user+'
    username += input('username: ')
    cliente.sendto(username.encode(), globals.servidor)
    return True


def protocolo():
    while True:

        entrada = input('\nSH >>> ')

        if entrada.split()[0].upper() == 'QUIT':
            cliente.sendall(entrada.encode())
            msg_server, globals.servidor = cliente.recvfrom(2048)
            print(msg_server.decode())
            break

        else:
            cliente.sendall(entrada.encode())
            msg_server, globals.servidor = cliente.recvfrom(2048)
            print(msg_server.decode())


if connect():
    protocolo()