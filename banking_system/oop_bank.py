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
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def nascimento(self):
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

    def exibir_historico(self):
        for transacao in self.historico.transacoes:
            print(f"{transacao['tipo']}: {transacao['valor']} - {transacao['data'].strftime('%d/%m/%Y')}")

    def __str__(self):
        return f"Agência: {self.agencia}\nNúmero: {self.numero}\nTitular: {self.cliente.nome}\n"

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, max_saques=3):
        self._limite = limite
        self._max_saques = max_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        n_saques = len([t for t in self.historico.transacoes if t["tipo"] == Saque.__name__])

        if n_saques >= self._max_saques:
            print("\nVocê já atingiu o limite de saques por hoje. Tente novamente amanhã\n")
        elif valor > self._limite:
            print(f"\nValor máximo para saques é {self._limite}\n")
        else:
            return super().sacar(valor)
        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

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

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

def sacar(contas, clientes):
    cpf = input("Digite seu CPF (somente números): ")
    cliente = consultar_cpf(cpf, clientes)
    #contas_cliente = listar_contas_cliente(contas, cliente)

    if not cliente:
        print("\nCliente não encontrado.\n")
    elif not listar_contas_cliente(contas, cliente):
        print("\nVocê não possui contas, cadastre uma primeiro.\n")
    else:
        valor = float(input("Valor do saque: "))
        transacao = Saque(valor)
        conta = listar_contas_cliente(contas, cliente)[0]
        cliente.realizar_transacao(conta, transacao)

def depositar(contas, clientes):
    cpf = input("Digite seu CPF (somente números): ")
    cliente = consultar_cpf(cpf, clientes)
    #contas_cliente = listar_contas_cliente(contas, cliente)

    if not cliente:
        print("\nCliente não encontrado.")
    elif not listar_contas_cliente(contas, cliente):
        print("\nVocê não possui contas, cadastre uma primeiro.\n")
    else:
        valor = float(input("Valor do deposito: "))
        transacao = Deposito(valor)
        conta = listar_contas_cliente(contas, cliente)[0]
        cliente.realizar_transacao(conta, transacao)

def cadastrar_cliente(clientes):
    cpf = input("Digite o CPF do cliente (somente números): ")
    if consultar_cpf(cpf, clientes):
        print("\nCliente já cadastrado.\n")
    else:
        nome = input("Nome completo: ")
        endereco = input("Endereço: ")
        nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        clientes.append(
            PessoaFisica(cpf, nome, nascimento, endereco)
        )
        print("\nCliente cadastrado com sucesso!\n")

def criar_conta(contas, clientes):
    cpf = input("Digite o CPF do cliente (somente números): ")
    cliente = consultar_cpf(cpf, clientes)

    if not cliente:
        print("\nCliente não cadastrado; realize o cadastro primeiro.\n")
    else:
        numero = f"{(len(contas) + 1):04}"
        conta = ContaCorrente.nova_conta(cliente, numero)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print("Conta cadastrada com sucesso!\n")
        print(conta)
        return True

def listar_contas_cliente(contas, cliente):
    cpf = cliente.cpf
    contas_cliente = [c for c in contas if c.cliente.cpf == cpf]
    return contas_cliente if contas_cliente else None

def exibir_extrato(contas, clientes):
    cpf = input("Digite o CPF do cliente (somente números): ")
    cliente = consultar_cpf(cpf, clientes)
    conta = listar_contas_cliente(contas, cliente)[0]
    conta.exibir_historico()

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

    while True:
        opcao = menu()

        match opcao:
            case 'd':
                depositar(contas, clientes)
            case 's':
                sacar(contas, clientes)
            case 'e':
                exibir_extrato(contas, clientes)
            case 'l':
                cadastrar_cliente(clientes)
            case 't':
                criar_conta(contas, clientes)
            case 'r':
                pass
            case 'q':
                break
            case _:
                print("Opção inválida.\n")

if __name__ == '__main__':
    main()
