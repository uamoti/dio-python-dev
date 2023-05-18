#!/usr/bin/python3

from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente:

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):

    def __init__(self, cpf, nome, nascimento, endereco):
        self._cpf = cpf
        self._nome = nome
        self._nascimento = nascimento
        super().__init__(endereco)

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):

        if valor > self._saldo:
            print("Você não possui saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("Valor inválido. Tente novamente.")

        return False

    def depositar(self, valor):

        if valor < 0:
            print("Valor inválido. Tente novamente.")
            return False
        else:
            self._saldo += valor
            return True

    # def __str__(self):
    #     return f"{self.__class__.__name__}: {', '.join([f'{key}: {value}' for key, value in self.__dict__.items()])}"

class ContaCorrente(Conta):

    def __init__(self, limite, max_saques, numero, cliente, saldo):
        self._limite = limite
        self._max_saques = max_saques
        super().__init__(numero, cliente, saldo)

class Historico:

    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now()
            }
        )

class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):

        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):

        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

def menu():

    menu = """\
        =========
        Banco DIO
        =========
        [ d ] Depositar
        [ s ] Sacar
        [ e ] Extrato
        [ l ] Cadastrar cliente
        [ t ] Cadastrar conta
        [ q ] Sair

        => """

    return input(textwrap.dedent(menu))

def main():

    def sacar():
        pass

    def depositar():
        pass

    def criar_cliente():
        pass

    def criar_conta():
        pass

    def listar_contas():
        pass

    def exibir_extrato():
        pass
