import socket
import threading
import time
from threading import Thread, Semaphore
from style import style
from arvore import AVLTree
from lista import Lista
import globals

globals.chat = ''

HOST = 'localhost'
PORT = 1500

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
origem = (HOST, PORT)
servidor.bind(origem)

arvore = AVLTree()
lista = Lista()
lista.insere_no_inicio('Usuarios:\n')
semaforoA = Semaphore(1)
semaforoL = Semaphore(1)

print('\n-- Say Hello --\n')


def protocolo(entrada, cliente):

    if entrada.split('+')[0] == 'user':
        aux = entrada.split('+')[1]
        globals.usuario = aux
        semaforoL.acquire()
        lista.inserir(lista.cabeca, usuario)
        semaforoL.release()
        print(f'{style.BLUE}• Cliente {aux} conectado{style.RESET}')

    else:
        comando = entrada.split()[0].upper()
        
        if comando == 'CREATE':
            nome = ''
            for i in entrada.split()[1:]:
                nome += f'{i} '
            if arvore.busca(nome):
                msg = f'{style.RED}400 -ERR chat já existente{style.RESET}'
            else:
                semaforoA.acquire()
                arvore.insert(nome)
                semaforoA.release()
                print(f'{style.BLUE}Criando chat...{style.RESET}')
                time.sleep(1)
                print(f'{style.GREEN}Chat criado: {nome}{style.RESET}')
                msg = f'{style.GREEN}200 +OK chat {nome}criado{style.RESET}'
            servidor.sendto(msg.encode(), cliente)


        elif comando == 'DELETE':
            nome = ''
            for i in entrada.split()[1:]:
                nome += f'{i} '
            if arvore.busca(nome):
                semaforoA.acquire()
                arvore.delete(nome)
                semaforoA.release()
                print(f'{style.BLUE}Deletando chat...{style.RESET}')
                time.sleep(1)
                print(f'{style.GREEN}Chat deletado: {nome}{style.RESET}')
                time.sleep(1)
                msg = f'{style.GREEN}200 +OK chat deletado{style.RESET}'
            else:
                msg = f'{style.RED}400 --ERR este chat não existe{style.RESET}'
            servidor.sendto(msg.encode(), cliente)


        elif comando == 'JOIN':
            nome = ''
            for i in entrada.split()[1:]:
                nome += f'{i} '
            globals.chat = nome
            if arvore.busca(nome):
                semaforoL.acquire()
                lista.remover(globals.usuario)
                lista.inserir(lista.cabeca, globals.usuario, nome)
                semaforoL.release()
                time.sleep(0.5)
                msg = f'{style.GREEN}200 +OK entrando no chat{style.RESET}'
            else:
                msg = f'{style.RED}400 -ERR este chat não existe{style.RESET}'
            servidor.sendto(msg.encode(), cliente)


        elif comando == 'CHATS':
            if arvore.isEmpty():
                msg = f'{style.RED}400 -ERR servidor ainda não possui chats{style.RESET}'
                servidor.sendto(msg.encode(), cliente)
            else:
                msg = f'{style.GREEN}200 +OK\n{style.RESET}'
                preordem = arvore.preordem()
                out = f'{msg}\n{preordem}'
                servidor.sendto(out.encode(), cliente)


        elif comando == 'MSG':
            msg = ''
            for i in entrada.split()[1:]:
                msg += f'{i} '
            print(f'{globals.usuario} ( {globals.chat}) → {msg}')
            out = ''
            servidor.sendto(out.encode(), cliente)


        elif comando == 'QUIT':
            semaforoL.acquire()
            lista.remover(globals.usuario)
            semaforoL.release()
            time.sleep(1)
            print(f'{style.BLUE}• Cliente {globals.usuario} desconectado{style.RESET}')
            servidor.sendto(f'{style.GREEN}200 +OK\n{style.RESET}\n--- Say Goodbye  ---\n'.encode(), cliente)


        else:
            msg = f'''\nDigite um comando válido.
{'='*30}
CREATE → criar um chat
DELETE → deletar um chat
JOIN → entrar em um chat
CHATS → imprime a árvore de chats
QUIT → encerra a conexão'''
            servidor.sendto(msg.encode(), cliente)


while True:
    usuario, cliente = servidor.recvfrom(2048)
    usuario = usuario.decode()
    threading.Thread(target=protocolo, args=(usuario, cliente)).start()