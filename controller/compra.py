import questionary
import numpy as np
from time import sleep
from tabulate import tabulate
from model.model import Compra, Fornecedor
from auxiliar import ValidadorValorNulo, ValidadorNumero, ValidarOpcao, ValidarAutoComplete
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print
from controller.item_compra import inserir_item_compra, listar_itens_compra

compra_global = Compra()

def consultar_fonecedores() -> list[tuple]:
    fornecedor = Fornecedor()
    fornecedores = fornecedor.consultar_fornecedor_geral()
    return fornecedores 

def buscar_id_fornecedor(nome_fornecedor) -> int:
    fornecedores = consultar_fonecedores()
    for fornecedor in fornecedores:
        if nome_fornecedor in fornecedor:
            id_fornecedor = fornecedor[0]
    return id_fornecedor

def consultar_id_compra(id_compra):
    resultado = compra_global.consultar_compra(id_compra=id_compra)
    return resultado

def gerar_compra():
    
    while True:

        cabecalho()

        nome_fornecedores = [nome[1] for nome in consultar_fonecedores()]

        fornecedor = questionary.autocomplete(message="Selecione o fornecedor: ",
                                              choices=nome_fornecedores,
                                              validate=ValidarAutoComplete(nome_fornecedores),
                                              style=estilo_questionary(),
                                              ).ask()
        
        id_fornecedor = buscar_id_fornecedor(nome_fornecedor=fornecedor)

        nova_compra = Compra(id_forncedor=id_fornecedor)
        mensagem, id_compra = nova_compra.cadastrar_compra()

        questionary.print(text=mensagem,
                          style=estilo_print())

        inserir_item_compra(id_compra=id_compra)

        listar_itens_compra(id_compra=id_compra)

        questao = questionary.confirm(message="Deseja finalizar a compra?").ask()

        if questao:
            finalizar_compra()
        else:
            break

def listar_compras():
    
    while True:

        resultado = compra_global.consultar_compra_geral()

        resultado_tratado = np.delete(resultado,np.r_[5,6,9:13], axis=1)

        questionary.print(text=tabulate(tabular_data=resultado_tratado, 
                                        headers=["ID","Data Compra", "Valor Total", "Valor Pago", "Valor Desconto", "ID F", "Fornecedor"],
                                        tablefmt="double_outline"))

        questionary.print(text="Informe o código da compra para detalhar, ou 0 para voltar.",
                          style=estilo_print())
        
        id_compra =int(questionary.text(message="Digite: ",
                         style=estilo_questionary(),
                         validate=ValidadorNumero).ask())
        
        if id_compra == "0":
            break

        resposta = consultar_id_compra(id_compra=id_compra)

        if isinstance(resposta, tuple):
            listar_itens_compra(id_compra=id_compra)
            questionary.press_any_key_to_continue(message="...")
        else:
            questionary.print(text=resposta,
                              style=estilo_print())
            questionary.press_any_key_to_continue(message="...")

def atulizar_compra():
    pass

def finalizar_compra():
    pass

def cancelar_compra():
    pass

def compra():
    
    while True:

        cabecalho()

        opcoes = [
            {"name":"Gerar Nova Compra", "value":"1"},
            {"name":"Atualizar Compra", "value":"2"},
            {"name":"Listar Compras", "value":"3"},
            questionary.Separator(),
            {"name":"Voltar", "value":"4"}
        ]

        selecao = questionary.select(message="O que deseja fazer: ",
                                     choices=opcoes,
                                     instruction=" ",
                                     qmark=" ",
                                     style=estilo_questionary()).ask()
        
        match selecao:
            case "1":
                gerar_compra()
            case "2":
                atulizar_compra()
            case "3":
                listar_compras()
            case "4":
                break