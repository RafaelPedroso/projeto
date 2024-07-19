from time import sleep
import questionary
from tabulate import tabulate
from  model.model import Cidade
from auxiliar import ValidadorValorNulo, ValidadorNumero
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

cidade_global = Cidade()

def cadastrar_nova_cidade():
    while True:

        cabecalho()

        questoes = questionary.form(
            nome = questionary.text("Cidade: ",
                                validate=ValidadorValorNulo),
            uf = questionary.text("Estado: ",
                              validate=ValidadorValorNulo)
        ).ask()

        nova_cidade = Cidade(**questoes)
        nova_cidade.cadastrar_cidade()
        questao = questionary.confirm("Deseja cadastrar outra cidade?",
                                      style=estilo_questionary()).ask()
        if not questao:
            break

def listar_cidades():
    while True:

        cabecalho()

        resultado = cidade_global.consultar_cidade_geral()
        print(tabulate(resultado,
                    headers=["ID","Cidade", "UF"],
                    tablefmt="double_outline"))
        print("O que deseja fazer: 1-ALTERAR / 2-EXCLUIR / 3-VOLTAR")
        opcao = input()
        match opcao:
            case "1":
                alterar_cidade()
            case "2":
                excluir_cidade()
            case "3":
                break
            case _:
                print("Selecione uma opção válida.")

def alterar_cidade():
    while True:
        try:
            id_cidade = questionary.text(message="Informe o código da cidade: ",
                                         style=estilo_questionary()).ask()

            if id_cidade:
                id_cidade = int(id_cidade)
                resultado = cidade_global.consultar_cidade(id_cidade=id_cidade)

                print(tabulate([resultado],
                    headers=["ID","Cidade", "UF"],
                    tablefmt="double_outline"))

                print("")

                if isinstance(resultado, tuple):
                    questoes = questionary.form(
                        novo_nome = questionary.text(message="Cidade: ",
                                                     default=resultado[1],
                                                     style=estilo_questionary()),
                        novo_uf = questionary.text(message="Estado: ", default=resultado[2],
                                                   style=estilo_questionary())
                    ).ask()

                    mensagem = cidade_global.alterar_cidade(id_cidade=id_cidade,
                                                          **questoes)
                    questionary.print(mensagem,
                                      style=estilo_print())
                    sleep(2)
                    break

                questionary.print(resultado,
                                  style=estilo_print())
            else:
                break

        except ValueError:
            questionary.print(text="Infomar um código válido da cidade.",
                              style=estilo_print())

def excluir_cidade():
    while True:
        try:
            id_cidade = int(questionary.text(message="Informe o código da cidade: ",
                                         style=estilo_questionary(),
                                         validate=ValidadorNumero).ask())

            resultado = cidade_global.consultar_cidade(id_cidade=id_cidade)
            resposta = questionary.confirm(message="Deseja excluir a cidade?",
                                            default=f"{resultado[0]} - {resultado[1]} - {resultado[2]}",
                                            style=estilo_questionary()).ask()
            if resposta:
                mensagem = cidade_global.excluir_cidade(id_cidade=id_cidade)
                questionary.print(text=mensagem,
                                    style=estilo_print())
                sleep(2)
                break
        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())

def cidade():

    while True:

        cabecalho()

        opcoes = [
            {"name":"Cadastrar Nova Cidade","value":"1"},
            {"name":"Listar Cidades","value":"2"},
            questionary.Separator(),
            {"name":"Voltar","value":"3"},
        ]

        selecao = questionary.select(message="O que deseja fazer: ",
                                    choices=opcoes,
                                    instruction=" ",
                                    qmark=" ",
                                    style=estilo_questionary(),).ask()

        match selecao:
            case "1":
                cadastrar_nova_cidade()

            case "2":
                listar_cidades()

            case "3":
                break
