saldo = 0
limite = 500
extrato_str = ""
numero_saques = 0
LIMITE_SAQUES = 3

menu ="""
      >>>Menu<<<
    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [0] - Sair
    """

def depositar(valor):
    global saldo, extrato_str
    if valor > 0:
        saldo += valor
        print("Deposito realizado com sucesso")
        extrato_str += f"Depósito de R$ {valor:.2f}\n"

def sacar(valor):
    global saldo, LIMITE_SAQUES, numero_saques, extrato_str
    if numero_saques == LIMITE_SAQUES:
        print("Limite de saques excedidos")
    elif valor > saldo:
        print("Não é possivel efetuar o saque por falta de saldo")
    elif valor > 500:
        print("Valor limite de 500 reais")

    else:
        saldo -= valor
        numero_saques += 1
        print("Saque realizado com sucesso")
        extrato_str += f"Saque de R$ {valor:.2f}\n"

def extrato(valor):
    global saldo, extrato_str
    print("Operações realizadas:")
    print(extrato_str)
    print("Seu saldo é R$ {:.2f}".format(saldo))

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Digite o valor a ser depositado: "))
        depositar(valor)

    elif opcao == "2":
        valor = float(input("Digite o valor a ser sacado: "))
        sacar(valor)

    elif opcao == "3":
        extrato(valor)

    elif opcao == "0":
        print("Obrigado por usar o programa")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")
    


