#!/usr/bin/python3

from abc import ABC


class Cliente:

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        pass

    def adicionar_conta(self, conta):
        pass

class PessoaFisica(Cliente):

    def __init__(self, cpf, nome, nascimento, endereco):
        self._cpf = cpf
        self._nome = nome
        self._nascimento = nascimento
        super().__init__(endereco)

class Conta:

    def __init__(self, numero, cliente, historico, saldo=0):
        self._saldo = saldo
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = historico

    def saldo(self):
        return self._saldo

    def nova_conta(self, cliente, numero):
        pass

    def sacar(self, valor):
        pass

    def depositar(self, valor):
        pass

class ContaCorrente(Conta):

    def __init__(self, limite, max_saques, numero, cliente, saldo):
        self._limite = limite
        self._max_saques = max_saques
        super().__init__(numero, cliente, saldo)

class Historico:

    def adicionar_transacao(self, transacao):
        pass

class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):

    def registrar(self, conta)

class Saque(Transacao):
    pass
