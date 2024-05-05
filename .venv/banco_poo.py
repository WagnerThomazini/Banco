from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso")
            return True
        else:
            print("\nValor inválido")
            return False

    def sacar(self, valor):
        if valor > 0:
            if valor > self._saldo:
                print("\nSaldo insuficiente")
                return False
            else:
                self._saldo -= valor
                print("\nSaque realizado com sucesso")
                return True
        else:
            print("\nValor inválido")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if valor > self._limite:
            print("\nO Valor do saque excede o limite")
            return False

        elif valor > self._saldo:
            print("\nSaldo insuficiente")
            return False

        elif self._saques_realizados >= self._limite_saques:
            print("\nLimite de saques excedidos")
            return False

        self._saques_realizados += 1
        return super().sacar(valor)

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu_string = """
      >>>Menu<<<
    [1] - Criar usuario
    [2] - Listas usuario 
    [3] - Criar conta
    [4] - Listar conta
    [5] - Depositar
    [6] - Sacar
    [7] - Extrato
    [0] - Sair
    """
    return input((menu_string))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\nCliente não possui conta! ")
        return

    return cliente._contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cpf = cpf.replace("-", "").replace(".", "")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cpf = cpf.replace("-", "").replace(".", "")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cpf = cpf.replace("-", "").replace(".", "")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\nEXTRATO ")
    transacoes = conta.historico._transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input('Digite o CPF: ')
    cpf = cpf.replace("-", "").replace(".", "")
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]

    if clientes_filtrados:
        print("\nJá existe esse CPF cadastrado! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento dd-mm-aaaa: ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!!! ")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cpf = cpf.replace("-", "").replace(".", "")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\nConta criada com sucesso!!! ")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
                   Agência:\t{conta.agencia}
                   C/C:\t\t{conta.numero}
                   Titular:\t{conta.cliente._nome}
               """
        print((linha))

def listar_usuarios(clientes):
    for cliente in clientes:
        linha = f"""\
                   Usuario:\t{cliente._nome}
                   CPF:\t\t{cliente._cpf}
                   Endereco:\t{cliente._endereco}                   
                   """
        print(linha)

clientes = []
contas = []

while True:
    opcao = menu()

    if opcao == "1":
        criar_cliente(clientes)

    elif opcao == "2":
        listar_usuarios(clientes)

    elif opcao == "3":
        numero_conta = len(contas) + 1
        criar_conta(numero_conta, clientes, contas)

    elif opcao == "4":
        listar_contas(contas)

    elif opcao == "5":
        depositar(clientes)

    elif opcao == "6":
        sacar(clientes)

    elif opcao == "7":
        exibir_extrato(clientes)

    elif opcao == "0":
        print("Obrigado por usar o programa")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")
