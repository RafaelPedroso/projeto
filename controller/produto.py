import questionary
from tabulate import tabulate
from time import sleep
from model.model import Produto, Fabricante
from auxiliar import ValidadorValorNulo, ValidarAutoComplete, ValidadorNumero, ValidarOpcao
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

produto_global = Produto()

def consultar_fabricantes() -> list[tuple]:
    fabricante = Fabricante()
    fabricantes = fabricante.consultar_fabricante_geral()
    return fabricantes

def buscar_id_fabricante(nome_fabricante) -> int:
    fabricantes = consultar_fabricantes()
    for fabricante in fabricantes:
        if nome_fabricante in fabricante:
            id_fabricante = fabricante[0]
    return id_fabricante

def cadastrar_novo_produto() -> None:
    
    while True:

        cabecalho()

        nomes_fabricantes = [nome[1] for nome in consultar_fabricantes()]

        questoes = questionary.form(
            descricao = questionary.text(message="Descrição do produto: ",
                                         validate=ValidadorValorNulo,
                                         qmark="*",
                                         style=estilo_questionary()),
            marca = questionary.text(message="Marca: ",
                                     validate=ValidadorValorNulo,
                                     qmark="*",
                                     style=estilo_questionary()),
            fabricante = questionary.autocomplete(message="Digite o nome do fabricante:",
                                                  choices=nomes_fabricantes,
                                                  validate=ValidarAutoComplete(nomes_fabricantes),
                                                  style=estilo_questionary())
        ).ask()

        id_fabricante = buscar_id_fabricante(questoes.get("fabricante"))

        questoes = {**questoes,
                    "id_fabricante":id_fabricante}
        novo_produto = Produto(**questoes)
        mensagerm = novo_produto.cadastrar_produto()

        print()

        questionary.print(text=mensagerm,
                          style=estilo_print())
        print()

        questao = questionary.confirm(message="Deseja cadastrar ou produto?",
                                      style=estilo_questionary()).ask()
        
        if not questao:
            break

def listar_produtos() -> None:
    
    while True:

        cabecalho()

        resultado = produto_global.consultar_produto_geral()
        #(1, 'Nvidia RTX 3090', 67.0, 161.79, 0.0, 'Nvidia', 1014, 1014, 'Nvidia', 'www.nvidia.com.br')
        resultado_tratado = [(valor[0], valor[1], valor[2], valor[3], valor[4], valor[5], valor[8]) for valor in resultado]

        questionary.print(text=tabulate(tabular_data=resultado_tratado,
                                       headers=["ID", "Descrição", "Estoque", "Valor Compra", "Valor Venda", "Marca", "Fabricante"],
                                       tablefmt="double_outline"))
        
        print()

        questionary.print(text="O que deseja fazer: 1-ALTERAR / 2-EXCLUIR / 3-VOLTAR: ",
                          style=estilo_print())
        
        print()

        opcao = questionary.text(message="Digite a opção: ",
                                 validate=ValidarOpcao(["1","2","3"]),
                                 qmark="*",
                                 style=estilo_questionary()).ask()
        
        match opcao:
            case "1":
                alterar_produto()
            case "2":
                excluir_produto()
            case "3":
                break

def alterar_produto() -> None:
    
    while True:
        try:
            nomes_fabricantes = [nome[1] for nome in consultar_fabricantes()]

            id_produto = int(questionary.text(message="Informe o código do produto: ",
                                              validate=ValidadorNumero,
                                              qmark="*",
                                              style=estilo_questionary()).ask())
            
            resultado = produto_global.consultar_produto(id_produto=id_produto)

            if isinstance(resultado, tuple):
                questoes = questionary.form(
                    descricao = questionary.text(message="Descrição do produto",
                                                 default=resultado[1],
                                                 qmark="*",
                                                 style=estilo_questionary()),
                    marca = questionary.text(message="Marca: ",
                                             default=resultado[5],
                                             qmark="*",
                                             style=estilo_questionary()),
                    fabricante = questionary.autocomplete(message="Fabricante: ",
                                                          choices=nomes_fabricantes,
                                                          default=resultado[8],
                                                          qmark="*",
                                                          validate=ValidarAutoComplete(nomes_fabricantes),
                                                          style=estilo_questionary())
                ).ask()

                id_fabricante = buscar_id_fabricante(questoes.get("fabricante"))

                questoes = {
                    **questoes,
                    "id_fabriante":id_fabricante
                }

                mensagem = produto_global.alterar_produto(id_produto=id_produto,
                                                          **questoes)
                
                questionary.print(text=mensagem,
                                  style=estilo_print())
                
                sleep(2)
                break

            else:
                questionary.print(text=resultado,
                                    style=estilo_print())
        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())

def excluir_produto() -> None:
    
    while True:
        try:
            id_produto = int(questionary.text(message="Informe o código do produto: ",
                                              validate=ValidadorNumero,
                                              qmark="*",
                                              style=estilo_questionary()).ask())
            
            resultado = produto_global.consultar_produto(id_produto=id_produto)
            resposta = questionary.confirm(message="Deseja excluir o produto?",
                                           default=f"{resultado[0]} - {resultado[1]}",
                                           style=estilo_questionary()).ask()
            if resposta:
                mensagem = produto_global.excluir_produto(id_produto=id_produto)
                questionary.print(text=mensagem,
                                  style=estilo_print())
                sleep(2)
                break

        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())

def produto() -> None:
    
    while True:
        
        cabecalho()

        opcoes = [
            {"name":"Cadastrar Novo Produto","value":"1"},
            {"name":"Listar Produtos","value":"2"},
            questionary.Separator(),
            {"name":"Voltar","value":"3"}
        ]

        selecao = questionary.select(message="O que deseja fazer:",
                                     choices=opcoes,
                                     instruction=" ",
                                     qmark=" ",
                                     style=estilo_questionary()).ask()
        
        match selecao:
            case "1":
                cadastrar_novo_produto()
            case "2":
                listar_produtos()
            case "3":
                break