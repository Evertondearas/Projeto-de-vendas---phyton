import psycopg2, getpass, os, random
import matplotlib.pyplot as plt
import  numpy as np

def conexao_banco(usuario, senha):
    conexao = psycopg2.connect(
    host = "localhost",
    database = "Aut",
    user = usuario,
    password = senha)
    return conexao

def login():
    usuario = input("Login: ")
    senha = getpass.getpass("Senha: ")
    try:
        conexao = conexao_banco(usuario,senha)
        cursor = conexao.cursor()
        cursor.execute("SELECT verificar_cargo();")
        cargo = cursor.fetchone()
        return [cargo[0], conexao]
    except:
        print("Usuário ou senha inválidos!")
        exit();

def consulta_gerente(conexao):
    cursor = conexao.cursor()
    pesquisa = ("select * from gerente_view order by cod;")
    cursor.execute(pesquisa)
    resultado = cursor.fetchall()
    print("\n")
    for i in resultado:
        print("\nCódigo: ", i[0], "\nDescrição: ", i[1], "\npreço de custo: ", i[2], "\nPreço de Venda: ", i[3],"\nMargem: ", i[4],"%","\nQuantidade: ", i[5])
    print("\n")

def consulta_vendedor(conexao):
    cursor = conexao.cursor()
    pesquisa = ("select * from vendedor_view order by cod;")
    cursor.execute(pesquisa)
    resultado = cursor.fetchall()
    print("\n")
    for i in resultado:
        print("\nCódigo: ", i[0], "\nDescrição: ", i[1], "\nPreço de Venda: ", i[2], "\nQuantidade: ", i[3])
    print("\n")

def vender(cursor, ordem_s, cod_prod, qtd, valor_prod):
    venda = ("select vender_produto("+str(ordem_s)+","+str(cod_prod)+ ","+str(qtd)+ ","+str(valor_prod)+")")
    cursor.execute(venda)
    conexao.commit()

def realizar_venda(conexao):
    cursor = conexao.cursor()
    seguir_comprando = True
    valor_total = 0
    ordem_s = round(random.random()*1000)
    
    while(seguir_comprando):
        codigo = input("\nDigite o código do produto a ser comprado:")
        qtd = input("Digite a quantidade do produto:")

        pesquisa = ("SELECT verificar_disponibilidade("+codigo+","+qtd+");")
        cursor.execute(pesquisa) 
        disponibilidade = cursor.fetchone()

        if bool(disponibilidade[0]) == False:
            print("/nNão há produtos disponíveis para realizar a compra.\n")
            return realizar_venda(conexao)

        cursor.execute("SELECT preco_venda from produtos where cod = "+codigo+";")
        valor_produto = cursor.fetchone()

        valor_total += valor_produto[0] * int(qtd)
        seguir = input("\nDeseja Seguir Comprando [s ou n]:")

        if seguir not in['S','s']:
            seguir_comprando = False

        vender(cursor, ordem_s, codigo, qtd, valor_produto[0])

        print("\nO valor total da compra foi: "+str(round(valor_total,2)))

def exibir_grafico(conexao):
    vendedores = []
    valores_venda = []

    cursor = conexao.cursor()
    cursor.execute("select sum(valor) as total_venda, vendedor from vendas group by vendedor;")
    vendas = cursor.fetchall()

    for vendas in vendas:
        valores_venda.append(vendas[0])
        vendedores.append(vendas[1])
        
    nome_das_suas_colunas = vendedores
    valor_das_suas_colunas = valores_venda

    plt.style.use('Solarize_Light2')

    plt.bar(nome_das_suas_colunas, valor_das_suas_colunas, color = 'blue')

    plt.ylabel("Venda Total")
    plt.xlabel("Vendedores")
    plt.title("Vendas nos mês 05/23")
    plt.show()
    
    
def menu():
    os.system("cls")
    print("==========================")
    print("\tLojas Silva\t")
    print("==========================")
    print("[1] - Consultar produto")
    print("[2] - Vender produto")
    print("[3] - Mostrar gráfico")
    print("[4] - Sair")
    opcao = int(input("Digite a opção desejada:"))
    return opcao

def menu_vendedor(conexao):
    while(True):    
        opcao = menu()
        if opcao == 1:
            consulta_vendedor(conexao)
        elif opcao == 2:
            realizar_venda(conexao)
        elif opcao == 3:
            print("\nApenas Gerentes podem ver o gráfico de vendas.\n")
        else:
            exit()

def menu_gerente(conexao):
    os.system("cls")
    while(True):    
        opcao = menu()
    
        if opcao == 1:
            consulta_gerente(conexao)
        elif opcao == 2:
            realizar_venda(conexao)
        elif opcao == 3:
            exibir_grafico(conexao)
        else:
            exit()

[cargo, conexao] = login()

if cargo == "funcionarios":
   menu_vendedor(conexao)
   
else:
    menu_gerente(conexao)

conexao.close()
