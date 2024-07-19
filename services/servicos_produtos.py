from model.model import ItemCompra, Compra, Produto

produto = Produto()

def consultar_produtos() -> list[tuple]:
    produtos = produto.consultar_produto_geral()
    return produtos

def buscar_id_produto(nome_produto) -> int:
    produtos = consultar_produtos()
    for produto in produtos:
        if nome_produto in produto:
            id_produto = produto[0]
    return id_produto

def buscar_saldo_atual_produto(id_produto) -> int:
    saldo_produto = produto.consultar_produto(id_produto=id_produto)
    return saldo_produto[2]

def atualizar_produto(id_produto, valores) -> None:
    produto.alterar_produto(id_produto=id_produto, **valores)