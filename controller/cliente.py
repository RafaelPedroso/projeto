import questionary
import questionary.question
from tabulate import tabulate
from time import sleep
from model.model import Cliente, Cidade
from auxiliar import ValidadorValorNulo, ValidarAutoComplete, ValidarOpcao,ValidadorNumero
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

cliente_global = Cliente()

def consultar_cidades() -> tuple:
    cidade = Cidade()
    cidades = cidade.consultar_cidade_geral()
    return cidades

def bucar_id_cidade(nome_cidade) -> int:
    cidades = consultar_cidades()
    for cidade in cidades:
        if nome_cidade in cidade:
            id_cidade = cidade[0]
    return id_cidade

def cadastrar_novo_cliente() -> None:

    while True:

        cabecalho()

        nomes_cidades = [nome[1] for nome in consultar_cidades()]

        questoes = questionary.form(
            nome = questionary.text(message="Nome do cliente: ",
                                    validate=ValidadorValorNulo,
                                    qmark="*",
                                    style=estilo_questionary()
                                    ),
            endereco = questionary.text(message="Enderço: ",
                                        validate=ValidadorValorNulo,
                                        qmark="*",
                                        style=estilo_questionary()),                                        
            telefone = questionary.text(message="Telefone de contato: ",
                                        validate=ValidadorValorNulo,
                                        qmark="*",
                                        style=estilo_questionary()),                                        
            email = questionary.text(message="E-mail: ",
                                     validate=ValidadorValorNulo,
                                     qmark="*",
                                     style=estilo_questionary()),
            cidade = questionary.autocomplete(message="Digite o nome da cidade",
                                              choices=nomes_cidades,
                                              validate=ValidarAutoComplete(nomes_cidades),
                                              style=estilo_questionary())
        ).ask()

        id_cidade = bucar_id_cidade(nome_cidade=questoes.get("cidade"))

        questoes = {**questoes,
                    "id_cidade":id_cidade}
        novo_cliente = Cliente(**questoes)
        mensagem = novo_cliente.cadastrar_clinte()

        print()

        questionary.print(text=mensagem,
                          style=estilo_print())

        print()

        questao = questionary.confirm(message="Deseja cadastrar outro cliente?",
                                      style=estilo_questionary()).ask()
        
        if not questao:
            break

def listar_clientes() -> None:

    while True:

        cabecalho()

        resultado = cliente_global.consultar_cliente_geral()
        resultado_tratado = [(valor[0], valor[1], valor[2], valor[3], valor[4], valor[7]  ) for valor in resultado]

        questionary.print(text=tabulate(tabular_data=resultado_tratado,
                                        headers=["ID", "Clinte", "Endereço", "Telefone","E-mail", "Cidade"],
                                        tablefmt="double_outline"))

        print()

        questionary.print(text="O que deseja fazer: 1-ALTERAR / 2-EXCLUIR / 3-VOLTAR",
                          style=estilo_print())

        print()

        opcao = questionary.text(message="Digite a opção: ",
                                 validate=ValidarOpcao(["1","2","3"]),
                                 qmark="*",
                                 style=estilo_questionary()).ask()
        
        match opcao:
            case "1":
                alterar_cliente()
            case "2":
                excluir_cliente()
            case "3":
                break

def alterar_cliente() -> None:
    
    while True:
        try:
            nomes_cidades = [nome[1] for nome in consultar_cidades()]

            id_cliente = int(questionary.text(message="Informe o código do forncedor: ",
                                              validate=ValidadorNumero,
                                              qmark="*",
                                              style=estilo_questionary()).ask())
            
            resultado = cliente_global.consultar_cliente(id_cliente=id_cliente)

            if isinstance(resultado, tuple):
                questoes = questionary.form(
                    nome = questionary.text(message="Nome do cliente: ",
                                            default=resultado[1],
                                            qmark="*",
                                            style=estilo_questionary()),
                    endereco = questionary.text(message="Endereço: ",
                                                default=resultado[2],
                                                qmark="*",
                                                style=estilo_questionary()),
                    telefone = questionary.text(message="Telefone de contato: ",
                                                default=resultado[3],
                                                qmark="*",
                                                style=estilo_questionary()),
                    email = questionary.text(message="E-mail",
                                             default=resultado[4],
                                             qmark="*",
                                             style=estilo_questionary()),
                    cidade = questionary.autocomplete(message="Cidade: ",
                                                      choices=nomes_cidades,
                                                      default=resultado[7],
                                                      qmark="*",
                                                      validate=ValidarAutoComplete(nomes_cidades),
                                                      style=estilo_questionary())
                ).ask()

                id_cidade = bucar_id_cidade(questoes.get("cidade"))

                questoes = {
                    **questoes,
                    "id_cidade":id_cidade
                }

                mensagem = cliente_global.alterar_cliente(id_cliente=id_cliente,
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
            
def excluir_cliente() -> None:
    
    while True:
        try:
            id_cliente = int(questionary.text(message="Informe o código do cliente: ",
                                              validate=ValidadorNumero,
                                              qmark="*",
                                              style=estilo_questionary()).ask())
            
            resultado = cliente_global.consultar_cliente(id_cliente=id_cliente)
            resposta = questionary.confirm(message="Deseja excluir o cliente? ",
                                           default=f"{resultado[0]} - {resultado[1]}",
                                           style=estilo_questionary()).ask()
            if resposta:
                mensagem = cliente_global.excluir_cliente(id_cliente=id_cliente)
                questionary.print(text=mensagem,
                                  style=estilo_print())
                sleep(2)
                break

        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())

def cliente() -> None:
    
    while True:

        cabecalho()

        opcoes = [
            {"name":"Cadastrar Novo Cliente", "value": "1"},
            {"name":"Listar Clientes", "value":"2"},
            questionary.Separator(),
            {"name":"Voltar", "value":"3"},
        ]

        selecao = questionary.select(message="O que deseja fazer:",
                                     choices=opcoes,
                                     instruction=" ",
                                     qmark=" ",
                                     style=estilo_questionary()).ask()
        match selecao:
            case "1":
                cadastrar_novo_cliente()
            case "2":
                listar_clientes()
            case "3":
                break
