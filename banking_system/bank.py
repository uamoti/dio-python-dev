#!/usr/bin/python3

menu = '''
Banco DIO
----------------
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''
saldo = 0
LIMITE_POR_SAQUE = 500
LIMITE_NUM_SAQUES = 3
num_saques = 0
extrato = ''

while True:
    opcao = input(menu)

    if opcao == 'd':
        print('Depósito')
        valor = float(input('Qual o valor a ser depositado: '))
        saldo += valor
        extrato += f'Depósito de R$ {valor}\n'
    elif opcao == 's':
        if num_saques < LIMITE_NUM_SAQUES:
            print('Saque')
            valor = float(input('Valor do saque: '))
            if valor > 500:
                print('Valor máximo para saques é R$ 500')
                continue
            elif valor > saldo:
                print('Você não possui saldo suficiente')
            else:
                saldo -= valor
                num_saques += 1
                extrato += f'Saque de R$ {valor}\n'
        else:
            print('Você já realizou 3 saques hoje. Tente novamente amanhã.')
    elif opcao == 'e':
        print(extrato)
        print(f'Saldo: R$ {saldo}')
    elif opcao == 'q':
        break
    else:
        print('Opção inválida')
