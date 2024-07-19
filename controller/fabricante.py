import questionary
from time import sleep
from tabulate import tabulate
from model.model import Fabricante
from auxiliar import ValidadorValorNulo, ValidadorNumero, ValidarOpcao
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

fabricante_global = Fabricante()

def cadastrar_novo_fabricante():
    while True:

        cabecalho()

        try: 
            questoes = questionary.form(
                nome = questionary.text(message="Nome do Fabricante: ",
                                        validate=ValidadorValorNulo(),
                                        qmark="*",
                                        style=estilo_questionary()),
                site = questionary.text(message="Site do Fabricante: ",
                                        qmark="*",
                                        validate=ValidadorValorNulo,
                                        style=estilo_questionary())
            ).ask()

            novo_fabricante = Fabricante(**questoes)
            mensagem = novo_fabricante.cadastrar_fabricante()
            questionary.print(text=mensagem,
                              style=estilo_print())
            print()

            questao = questionary.confirm("Deseja cadastrar outro fabricante?",
                                          style=estilo_questionary()).ask()
            if not questao:
                break

        except ValueError:
            questionary.print(text=mensagem,
                              style=estilo_print())

def listar_fabricantes():
    while True:

        cabecalho()

        resultado = fabricante_global.consultar_fabricante_geral()

        questionary.print(text=tabulate(resultado,
                                        headers=["ID", "Fabricante", "Site"],
                                        tablefmt="double_outline"))
        
        print()

        questionary.print(text="O que deseja fazer: 1-ALTERAR / 2-EXCLUIR / 3-VOLTAR",
                          style=estilo_print())
        
        print()

        opcao = questionary.text(message="Digite a opção: ",
                                 style=estilo_questionary(),
                                 qmark="*",
                                 validate=ValidarOpcao(opcoes=["1","2","3"])).ask()
        match opcao:
            case "1":
                alterar_fabricante()
            case "2":
                excluir_fabricante()
            case "3":
                break

def alterar_fabricante():
    while True:
        try:
            id_fabricante = int(questionary.text(message="Informe o código do forncedor: ",
                                             validate=ValidadorNumero,
                                             qmark="*",
                                             style=estilo_questionary(),).ask())
            resultado = fabricante_global.consultar_fabricante(id_fabricante=id_fabricante)

            print()

            if isinstance(resultado, tuple):
                questionary.print(text=tabulate(tabular_data=[resultado],
                                            headers=["ID", "Fabricante", "Site"],
                                            tablefmt="double_outline"))
                print()

                questoes = questionary.form(
                    nome = questionary.text(message="Nome do Fabricante: ",
                                            default=resultado[1],
                                            qmark="*",
                                            style=estilo_questionary()
                                            ),
                    site = questionary.text(message="Site do Fabricante: ",
                                            default=resultado[2],
                                            qmark="*",
                                            style=estilo_questionary()
                                            )
                ).ask()

                mensagem = fabricante_global.alterar_fabricante(id_fabricante=id_fabricante,
                                                                **questoes)
                questionary.print(text=mensagem,
                                  style=estilo_print())
                
                sleep(2)
                break

            questionary.print(text=mensagem,
                              style=estilo_print())

        except ValueError:
            questionary.print(text="Informar um código válido do forncedor.",
                              style=estilo_print())

def excluir_fabricante():
    while True:
        try:
            id_fabricante = int(questionary.text(message="Informe o código do fabricante: ",
                                             validate=ValidadorValorNulo,
                                             style=estilo_questionary()).ask())
            
            resultado = fabricante_global.excluir_fabricante(id_fabricante=id_fabricante)
            resposta = questionary.confirm(message="Deseja exclluir o fabricante?",
                                           default=f"{resultado[0]} - {resultado[1]}",
                                           style=estilo_questionary()).ask()
            if resposta:
                mensagem = fabricante_global.excluir_fabricante(id_fabricante=id_fabricante)
                questionary.print(text=mensagem,
                                  style=estilo_print())
                
                sleep(2)
                break

        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())


def fabricante():
    while True:

        cabecalho()

        opcoes = [
            {"name":"Cadastrar Novo Fabricante", "value":"1"},
            {"name":"Listar Fabricantes", "value":"2"},
            questionary.Separator(),
            {"name":"Voltar", "value":"3"},
            ]

        selecao = questionary.select(message="O que deseja fazer: ",
                                     choices=opcoes,
                                     instruction=" ",
                                     qmark=" ",
                                     style=estilo_questionary()).ask()

        match selecao:
            case "1":
                cadastrar_novo_fabricante()
            case "2":
                listar_fabricantes()
            case "3":
                break
