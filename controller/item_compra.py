import questionary
from time import sleep
from datetime import datetime
from tabulate import tabulate
from model.model import ItemCompra, Compra
from auxiliar import ValidadorValorNulo, ValidadorNumero, ValidarOpcao, ValidarAutoComplete, ValidarItemInserido
from services.servicos_produtos import (consultar_produtos,
                                        buscar_id_produto,
                                        buscar_saldo_atual_produto,
                                        atualizar_produto)
from auxiliar import cabecalho
from auxiliar import estilo_questionary, estilo_print

item_compra_global = ItemCompra()

def consultar_compra(id_compra) -> tuple:
    compra = Compra()
    resultado = compra.consultar_compra(id_compra=id_compra)
    return resultado

def inserir_item_compra(id_compra):
    
    while True:
        nomes_produtos = [nome[1] for nome in consultar_produtos()]

        itens_inserido = listar_itens_compra(id_compra=id_compra)

        #questionary.print(text=resultado,style=estilo_print())

        print()

        produto = questionary.autocomplete(message="Selecione o produto: ",
                                            choices=nomes_produtos,
                                            validate=ValidarItemInserido(nomes_produtos=nomes_produtos,
                                                                        produtos_inserido=itens_inserido),
                                            style=estilo_questionary()).ask()
        quantidade = int(questionary.text(message="Digite a quantidade: ",
                                        validate=ValidadorNumero
                                        ).ask())
        vl_unitario = float(questionary.text(message="Digite o valor unitário : ",
                                        validate=ValidadorNumero
                                        ).ask())
        vl_total = vl_unitario * quantidade
        
        questionary.print(text=f"Valor total do produto: {vl_total}")

        id_produto = buscar_id_produto(nome_produto=produto)

        saldo_atual = buscar_saldo_atual_produto(id_produto=id_produto) + quantidade

        valores_produto = {"estoque":saldo_atual, "valor_compra":vl_unitario}

        atualizar_produto(id_produto=id_produto, valores=valores_produto)

        valores_itens = (quantidade, vl_total, id_produto, id_compra)

        novo_item_compra = ItemCompra(*valores_itens)

        atualizar_valor_compra(id_compra=id_compra, valor_total_item=vl_total)

        mensagem = novo_item_compra.cadastrar_item_compra()

        questionary.print(text=mensagem,
                            style=estilo_print())
        
        print()

        questao = questionary.confirm(message="Deseja inserir mais produto na compra?",
                                        style=estilo_questionary()).ask()
        
        if not questao:
            break

def listar_itens_compra(id_compra):

    cabecalho()

    compra = consultar_compra(id_compra=id_compra)
    data_venda = datetime.strptime(compra[1],"%Y-%m-%d %H:%M")
    data_venda = data_venda.strftime("%d/%m/%Y")

    questionary.print(text=f"Compra nº: {compra[0]}",
                    style=estilo_print())
    questionary.print(text=f"Data da Compra: {data_venda}")
    questionary.print(text=f"Fornecedor: {compra[5]} - {compra[8]}")
    questionary.print(text=f"Valor total compra: R$ {compra[2]}")
    
    questionary.print(text=f"{'-'*50}")

    questionary.print(text="Itens da compra.", 
                        style=estilo_print())
    
    print()

    resultado = item_compra_global.consultar_item_compra(id_compra=id_compra)

    itens_compra = []

    itens_inserido = []

    if isinstance(resultado, list):
        for item in resultado:
            itens_compra.append((item[3], item[13], item[1], item[15], item[2], item[17]))

        print(tabulate(tabular_data=itens_compra, headers=["Nº Item",
                                                "Cod. Produto",
                                                "Descrição do Produto",
                                                "Quantidade",
                                                "Valor Unitário",
                                                "valor Total",
                                                "Marca"
                                                ],
                                                tablefmt="double_outline",
                                                showindex=True))
        itens_inserido = [nome[1] for nome in itens_compra]
    else:
        questionary.print(text=resultado, 
                          style=estilo_print())
    return itens_inserido

def atualizar_valor_compra(id_compra, valor_total_item):

    compra = Compra()

    resultado = consultar_compra(id_compra=id_compra)

    valor_total_atualizado = valor_total_item + resultado[2]

    compra.alterar_compra(id_compra=id_compra, **{"valor_total":valor_total_atualizado})

def alterar_item_compra():
    pass

def excluir_item_compra():
    pass
