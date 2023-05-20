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

    @property
    def cpf:
        return self._cpf

    @property
    def nome:
        return self._nome

    @property
    def nascimento:
        return self._nascimento

class Conta:
    def __init__(self, cliente, numero):
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
            print("Saldo suficiente.")
            return False
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

    def __str__(self):
        return f"Agência: {self.agencia}\nNúmero: {self.numero}\nTitular: {self.cliente.nome}"

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, max_saques=3):
        self._limite = limite
        self._max_saques = max_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        n_saques = len([t for t in self.historico.transacoes if t["tipo"] == Saque.__name__])

        if n_saques >= max_saques:
            print("Você já atingiu o limite de saques por hoje. Tente novamente amanhã")
        elif valor > self._limite:
            print(f"Valor máximo para saques é {self._limite}")
        else:
            return super().sacar(valor)
        return False

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

def sacar():
    cpf = input("Digite seu CPF (somente números): ")
    cliente = consultar_cpf(cpf, clientes)
    contas_cliente = listar_contas_cliente(contas, cliente)

    if not cliente:
        print("Cliente não encontrado.")
    elif not contas_cliente:
        print("Você não possui contas, cadastre uma primeiro.")
    else:
        valor = float(print("Valor do saque: "))
        transacao = Saque(valor)
        conta = contas_cliente[0]
        cliente.realizar_transacao(conta, transacao)

def depositar():
    cpf = input("Digite seu CPF (somente números): ")
    cliente = consultar_cpf(cpf, clientes)
    contas_cliente = listar_contas_cliente(contas, cliente)

    if not cliente:
        print("Cliente não encontrado.")
    elif not contas_cliente:
        print("Você não possui contas, cadastre uma primeiro.")
    else:
        valor = float(print("Valor do saque: "))
        transacao = Deposito(valor)
        conta = contas_cliente[0]
        cliente.realizar_transacao(conta, transacao)

def criar_cliente():
    cpf = input("Digite o CPF do cliente (somente números): ")
    if consultar_cpf(cpf):
        print("Cliente já cadastrado.")
    else:
        nome = input("Nome completo: ")
        endereco = input("Endereço: ")
        nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        clientes.append(
            PessoaFisica(cpf, nome, nascimento, endereco)
        )
        print("Cliente cadastrado com sucesso!")

def criar_conta():
    cpf = input("Digite o CPF do cliente (somente números): ")
    cliente = consultar_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado; realize o cadastro primeiro")
    else:
        numero = f"{len(contas) + 1:04}"
        conta = ContaCorrente.nova_conta(cliente, numero)

def listar_contas_cliente(contas, cliente):
    cpf = cliente.cpf
    contas_cliente = [c for c in contas if conta.cliente.cpf == cpf]
    return contas_cliente if contas_cliente else None

def exibir_extrato():
    pass

def consultar_cpf(cpf, clientes):
    cliente = [c for c in clientes if c.cpf == cpf]
    return cliente[0] if cliente else None

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
        [ r ] Listar contas
        [ q ] Sair

        => """
    return input(textwrap.dedent(menu))

def main():
    clientes = []
    contas = []

    opcao = menu()

    match opcao:
        case 'd':
            pass
        case 's':
            pass
        case 'e':
            pass
        case 'l':
            pass
        case 't':
            pass
        case 'r':
            pass
        case 'q':
            break
        case _:
            print("Opção inválida.")

if __name__ == '__main__':
    main()
