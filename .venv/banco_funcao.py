AGENCIA = "0001"
usuarios = []
contas = []
saldo = 0
LIMITE = 500
extrato_str = ""
numero_saques = 0
LIMITE_SAQUES = 3

def criar_usuario(usuario):
  cpf = input("Informe o cpf: ")
  cpf = cpf.replace("-", "").replace(".","")
  usuario = filtrar_usuario (cpf, usuarios)

  if usuario:
        print("\n Já existe esse CPF cadastrado! ")
        return

  nome = input("Informe o nome completo: ")
  telefone = input("Informe o telefone: ")
  data_nascimento = input("Informe a data de nascimento dd-mm-aaaa: ")
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

  usuarios.append({"nome": nome, "telefone": telefone, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

  print("\n Usuario criado com sucesso!!! ")

def filtrar_usuario(cpf, usuarios):
  usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
  return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, conta, usuarios):
  cpf = input("Informe o CPF do usuário: ")
  cpf = cpf.replace("-", "").replace(".", "")
  usuario = filtrar_usuario(cpf, usuarios)

  if usuario:
      print("\n Conta criada com sucesso!")
      return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

  print("\n Usuário não encontrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
                   Agência:\t{conta['agencia']}
                   C/C:\t\t{conta['numero_conta']}
                   Titular:\t{conta['usuario']['nome']}
               """
        print((linha))

def listar_usuarios(usuarios):
    for usuario in usuarios:
        linha = f"""\
                   Usuario:\t{usuario['nome']}
                   CPF:\t\t{usuario['cpf']}
                   Telefone:\t{usuario['telefone']}
                   Endereco:\t{usuario['endereco']}                   
                   """
        print(linha)


def depositar(saldo, extrato_str, valor):
    if valor > 0:
        saldo += valor
        print("Deposito realizado com sucesso")
        extrato_str += f"Depósito de R$ {valor:.2f}\n"
        return saldo, extrato_str

def sacar(*, saldo, valor, extrato_str, LIMITE, numero_saques, LIMITE_SAQUES):
    if numero_saques == LIMITE_SAQUES:
        print("Limite de saques excedidos")
    elif valor > saldo:
        print("Não é possivel efetuar o saque por falta de saldo")
    elif valor > LIMITE:
        print("Valor limite de 500 reais")


    else:
        saldo -= valor
        numero_saques += 1
        print("Saque realizado com sucesso")
        extrato_str += f"Saque de R$ {valor:.2f}\n"
    return saldo, extrato_str, numero_saques


def extrato(saldo, /, *, extrato_str):
    print("Operações realizadas:")
    print(extrato_str)
    print("Seu saldo é R$ {:.2f}".format(saldo))
    return saldo, extrato_str

def menu():
    menu ="""
      >>>Menu<<<
    [1] - Criar Usuario
    [2] - Criar conta
    [3] - Listas contas
    [4] - Listar usuarios
    [5] - Depositar
    [6] - Sacar
    [7] - Extrato
    [0] - Sair
    """
    return input((menu))

while True:

    opcao = menu()
    if opcao == "1":
        criar_usuario(usuarios)

    elif opcao == "2":
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)

    elif opcao == "3":
        listar_contas(contas)

    elif opcao == "4":
        listar_usuarios(usuarios)

    elif opcao == "5":
        valor = float(input("Digite o valor a ser depositado: "))
        saldo, extrato_str = depositar(saldo, extrato_str, valor)

    elif opcao == "6":
        valor = float(input("Digite o valor a ser sacado: "))
        saldo, extrato_str, numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            extrato_str=extrato_str,
            LIMITE=LIMITE,
            numero_saques=numero_saques,
            LIMITE_SAQUES=LIMITE_SAQUES,
        )

    elif opcao == "7":
        saldo, extrato_str = extrato(saldo, extrato_str=extrato_str)

    elif opcao == "0":
        print("Obrigado por usar o programa")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")