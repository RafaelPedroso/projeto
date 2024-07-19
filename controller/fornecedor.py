import questionary
from tabulate import tabulate
from time import sleep
from model.model import Fornecedor, Cidade
from auxiliar import ValidadorValorNulo, ValidarAutoComplete, ValidadorNumero, ValidarOpcao
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

# [(1, 'Rocha Alves S.A.', 'Viaduto de Peixoto, 95', '+55 (86) 9 4522 5843', 'alvesmarina@example.org', 995, 995, 'Salto', 'SP')]
fornecedor_global = Fornecedor()

def consultar_cidades() -> tuple:
    cidade = Cidade()
    cidades = cidade.consultar_cidade_geral()
    return cidades

def buscar_id_cidade(nome_cidade) -> int:
    cidades = consultar_cidades()
    for cidade in cidades:
        if nome_cidade in cidade:
            id_cidade = cidade[0]
    return id_cidade

def cadastrar_novo_fornecedor() -> None:
    while True:

        cabecalho()

        nomes_cidades = [nome[1] for nome in consultar_cidades()]

        questoes = questionary.form(
            nome = questionary.text(message="Nome do Fornecedor:",
                                    validate=ValidadorValorNulo),
            endereco = questionary.text(message="Endereço:",
                                        validate=ValidadorValorNulo),
            telefone = questionary.text(message="Telefone de contado:",
                                        validate=ValidadorValorNulo),
            email = questionary.text("E-mail:",
                                     validate=ValidadorValorNulo),
            cidade = questionary.autocomplete(message="Digite o nome da cidade para escolher: ",
                                                choices=nomes_cidades,
                                                style=estilo_questionary(),
                                                validate=ValidarAutoComplete(nomes_cidades))
        ).ask()
        
        id_cidade = buscar_id_cidade(nome_cidade=questoes.get("cidade"))

        questoes = {**questoes,
                    "id_cidade":id_cidade}
        novo_fornecedor = Fornecedor(**questoes)
        mensagem = novo_fornecedor.cadastrar_fornecedor()

        questionary.print(text=mensagem,
                          style=estilo_print())

        questao = questionary.confirm(message="Deseja cadastrar outro fornecedor?",
                            style=estilo_questionary()).ask()
        if not questao:
            break        

def listar_fornecedores() -> None:

    while True:

        cabecalho()

        resultado = fornecedor_global.consultar_fornecedor_geral()
        resultado_tratado = [(valor[0], valor[1], valor[2], valor[3], valor[4], valor[7])for valor in resultado]

        questionary.print(text=tabulate(tabular_data=resultado_tratado,
                       headers=["ID", "Nome", "Endereço", "Telefone", "E-mail", "Cidade"],
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
                alterar_fornecedor()
            case "2":
                excluir_fornecedor()
            case "3":
                break

def alterar_fornecedor() -> None:

    while True:
        try:
            nomes_cidades = [nome[1] for nome in consultar_cidades()]

            id_fornecedor = int(questionary.text(message="Informe o código do fornecedor: ",
                                             style=estilo_questionary(),
                                             validate=ValidadorNumero).ask())

            resultado = fornecedor_global.consultar_fornecedor(id_fornecedor=id_fornecedor)
            
            if isinstance(resultado, tuple):
                questoes = questionary.form(
                    nome = questionary.text(message="Nome do fornecedor: ",
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
                    email = questionary.text(message="E-mail: ",
                                                default=resultado[4],
                                                qmark="*",
                                                style=estilo_questionary()),
                    cidade = questionary.autocomplete(message="Cidade: ", 
                                                      choices=nomes_cidades,
                                                      default=resultado[7],
                                                      qmark="*",
                                                      style=estilo_questionary())

                ).ask()

                id_cidade = buscar_id_cidade(questoes.get("cidade"))

                questoes = {
                    **questoes,
                    "id_cidade":id_cidade
                }

                mensagem = fornecedor_global.alterar_fornecedor(id_forncedor=id_fornecedor,
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

def excluir_fornecedor() -> None:
    
    while True:
        try:
            id_fornecedor = int(questionary.text(message="Informe o código do forncedor: ",
                                             validate=ValidadorNumero,
                                             style=estilo_questionary()).ask())
            resultado = fornecedor_global.consultar_fornecedor(id_fornecedor=id_fornecedor)
            resposta = questionary.confirm(message="Deseja excluir o forncedor? ",
                                           default=f"{resultado[0]} - {resultado[1]}",
                                           style=estilo_questionary()).ask()
            if resposta:
                mensagem = fornecedor_global.excluir_fornecedor(id_fornecedor=id_fornecedor)
                questionary.print(text=mensagem,
                                  style=estilo_print())
                sleep(2)
                break
            
        except ValueError:
            questionary.print(text="Informar um código válido.",
                              style=estilo_print())
            
def fornecedor() -> None:

    while True:

        cabecalho()

        opcoes = [
            {"name":"Cadastrar Novo Fornecedor","value":"1"},
            {"name":"Listar Forncedores","value":"2"},
            questionary.Separator(),
            {"name":"Voltar","value":"3"},
            ]
        
        selecao = questionary.select(message="O que deseja fazer:",
                                     choices=opcoes,
                                     instruction=" ",
                                     qmark=" ",
                                     style=estilo_questionary(),).ask()
        
        match selecao:
            case "1":
                cadastrar_novo_fornecedor()
            case "2":
                listar_fornecedores()
            case "3":
                break

        

