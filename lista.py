class ListaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class No:
    def __init__(self, user, chat=None):
        self.__user = user
        self.__chat = None
        self.__prox = None

    @property
    def user(self):
        return self.__user

    @property
    def prox(self):
        return self.__prox

    @property
    def chat(self):
        return self.__chat

    @user.setter
    def user(self, novo_user:str):
        self.__user = novo_user

    @prox.setter
    def prox(self, novo_prox:str):
        self.__prox = novo_prox

    @chat.setter
    def chat(self, chat):
        self.__chat = chat

    def __str__(self):
        return str(self.user)


class Lista:
    def __init__(self):
        self.__cabeca = None
        self.__tamanho = 0

    @property
    def cabeca(self):
        return self.__cabeca

    @property
    def tamanho(self):
        return self.__tamanho

    @cabeca.setter
    def cabeca(self, n_cabeca):
        self.__cabeca = n_cabeca

    @tamanho.setter
    def tamanho(self, n_tamanho):
        self.__tamanho = n_tamanho

    def insere_no_inicio(self, id):
        novo_no = No(id)
        novo_no.prox = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1

    def inserir(self, no_anterior, Key, chat=None):
        novo_no = No(Key)
        novo_no.chat = chat
        novo_no.prox = no_anterior.prox
        no_anterior.prox = novo_no
        self.tamanho += 1

    def buscar(self, chat):
        cursor = self.cabeca
        array = []
        while cursor != self.tamanho:
            if cursor.chat == chat:
                array.append(cursor)
                cursor = cursor.prox
        return array

    def remover(self, valor):
        if self.cabeca.user == valor:
            self.cabeca = self.cabeca.prox
        else:
            anterior = None
            cursor = self.cabeca
            while cursor and (cursor.user != valor):
                anterior = cursor
                cursor = cursor.prox
            if cursor:
                anterior.prox = cursor.prox
            else:
                anterior.prox = None
        self.tamanho -= 1

    def __str__(self) -> str:
        nada = ''
        cursor = self.cabeca
        str = ''
        while cursor:
            usuario = cursor.user.split('+')
            if usuario[0] == 'user':
                usuario = usuario[1]
            else:
                usuario = usuario[0]
            if usuario == 'Usuarios online:':
                str += f'\n{usuario}\n'
            else:
                if usuario in str:
                    pass
                else:
                    str += f'\n??? {usuario} ( {cursor.chat if cursor.chat is not None else nada})'
            cursor = cursor.prox
        return str