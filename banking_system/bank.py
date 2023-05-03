#!/usr/bin/python3

''' Parte 2:
Usar funções para modularizar o código;
Criar 2 novas funções: cadastrar usuário e cadastrar conta (vincular com usuário);
Função saque: kwargs only.
    Sugestão de argumentos: saldo, valor, extrato, limite, número de saques, limite de saques
    Sugestão de retorno: saldo, extrato
Função depósito: positional only.
    Sugestão de argumentos: saldo, valor, extrato
    Sugestão de retorno: saldo, extrato
Função extrato: positional and kwargs.
    Positional: saldo
    Kwargs: extrato
Fique a vontade para adicionar funções a mais, e.g. listar contas.
Armazenar usuários em uma lista.
O usuário é composto por nome, endereço e CPF.
Sugestão de endereço: logradouro, número, bairro, cidade e estado.
Somente números no CPF. Não pode haver dois usuários com o mesmo CPF.
Uma conta é composta por agência, número e usuário. O número é sequencial, começando por 1.
O número da agência é fixo, 0001.
Um usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário. '''

def saque(*, saldo, valor, extrato, max_n_saques, n_saques, limite_saque):

    if n_saques >= max_n_saques:
        print('Você já realizou 3 saques hoje. Tente novamente amanhã.')
        return saldo, extrato, n_saques
    elif valor > limite_saque:
        print('Valor máximo para saques é R$ 500')
        return saldo, extrato, n_saques
    elif valor > saldo:
        print('Você não possui saldo suficiente')
        return saldo, extrato, n_saques
    else:
        saldo -= valor
        n_saques += 1
        extrato += f'Saque de R$ {valor}\n'
        return saldo, extrato, n_saques

def deposito(saldo, valor, extrato, /):

    saldo += valor
    extrato += f'Depósito de R$ {valor}\n'
    return saldo, extrato

def extrato(saldo, /, *, extrato):

    print(extrato)
    print(f'Saldo: R$ {saldo}')

menu = '''\
Banco DIO
-------------
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''
saldo = 0
LIMITE_POR_SAQUE = 500
LIMITE_NUM_SAQUES = 3
n_saques = 0
extrato = ''

while True:
    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Qual o valor a ser depositado: '))
        # saldo += valor
        # extrato += f'Depósito de R$ {valor}\n'
        saldo, extrato = deposito(saldo, valor, extrato)
    elif opcao == 's':
        # if num_saques < LIMITE_NUM_SAQUES:
        #     valor = float(input('Valor do saque: '))
        #     if valor > 500:
        #         print('Valor máximo para saques é R$ 500\n')
        #         continue
        #     elif valor > saldo:
        #         print('Você não possui saldo suficiente\n')
        #     else:
        #         saldo -= valor
        #         num_saques += 1
        #         extrato += f'Saque de R$ {valor}\n'
        # else:
        #     print('Você já realizou 3 saques hoje. Tente novamente amanhã.\n')
        valor = float(input('Valor do saque: '))
        saldo, extrato, n_saques = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            max_n_saques=LIMITE_NUM_SAQUES,
            n_saques=n_saques,
            limite_saque=LIMITE_POR_SAQUE
        )
    elif opcao == 'e':
        print(extrato)
        print(f'Saldo: R$ {saldo}\n')
    elif opcao == 'q':
        break
    else:
        print('Opção inválida\n')
