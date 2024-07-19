from datetime import datetime
from connection.conexao import Banco
from auxiliar import validar_id

class Cidade:

    def __init__(self, **kargs) -> None:
        self.nome = kargs.get("nome")
        self.estado = kargs.get("uf")
        self.tabela = "cidade"

    def consultar_cidade(self, id_cidade):
        if not validar_id(id=id_cidade):
            raise ValueError("Informe um código válido da cidade")

        with Banco() as banco:
            try:
                condicao = f"id = {id_cidade}"
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao)
                if resultado:
                    return resultado[0]
                return f"Cidade não localizado com o id: {id_cidade}"
            except RuntimeError as e:
                return f"Erro ao consultar a cidade: {e}"

    def consultar_cidade_geral(self) -> tuple:
        with Banco() as banco:
            try:
                resultado = banco.consultar(tabela=self.tabela)
                return resultado
            except RuntimeError as e:
                return f"Erro ao consultar as cidades: {e}"

    def cadastrar_cidade(self) -> str:
        with Banco() as banco:
            try:
                valores = (self.nome, self.estado)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                print(f"Cidade cadastrada com sucesso.\nCódigo: {novo_id}")
            except RuntimeError as e:
                print(f"Erro ao cadastrar a cidade. Erro: {e}")

    def excluir_cidade(self, id_cidade):
        if not validar_id(id=id_cidade):
            raise ValueError("Informe um código válido da cidade")

        with Banco() as banco:
            try:
                condicao = f"id = {id_cidade}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return "Registro excluído com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir a cidade código {id_cidade}. Erro: {e}"

    def alterar_cidade(self, id_cidade, **kargs):
        if not validar_id(id=id_cidade):
            raise ValueError("Informe um código válido da cidade")

        with Banco() as banco:
            try:
                resultado = self.consultar_cidade(id_cidade)

                if resultado:
                    self.nome = kargs.get("novo_nome") or resultado[1]
                    self.estado = kargs.get("novo_uf") or resultado[2]
                    valores = (self.nome, self.estado)
                    condicao = f"id = {id_cidade}"
                    banco.executar_comando(tipo="update",
                                                tabela=self.tabela,
                                                condicao=condicao,
                                                valores=valores)
                    return f"Fabricante {self.nome} alterado com sucesso."
                else:
                    return f"Não foi localizado cidade com o código: {id_cidade}"
            except RuntimeError as e:
                return f"Erro ao alterar a cidade código {id_cidade}. Erro {e}"

class Fabricante:

    def __init__(self, **kargs) -> None:
        self.nome = kargs.get("nome")
        self.site = kargs.get("site")
        self.tabela = "fabricante"

    def consultar_fabricante(self, id_fabricante) -> tuple:
        if not validar_id(id=id_fabricante):
            raise ValueError("Informe um código válido do fabricante")

        with Banco() as banco:
            try:
                condicao = f"id = {id_fabricante}"
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao)
                if resultado:
                    return resultado[0]
                return f"Fabricante não localizado com o código código {id_fabricante}"
            except RuntimeError as e:
                return f"Erro ao consultar o fabricante: {e}"

    def consultar_fabricante_geral(self) -> list[tuple]:
        with Banco() as banco:
            try:
                resultado = banco.consultar(tabela=self.tabela)
                if resultado:
                    return resultado
                return "Não há fabricantes para serem listados."
            except RuntimeError as e:
                return f"Erro ao consultar os fabricantes: {e}"

    def cadastrar_fabricante(self) -> str:
        with Banco() as banco:
            try:
                valores = (self.nome, self.site)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                return "Fabricante cadastrado com sucesso."
            except RuntimeError as e:
                return f"Erro ao inserir o fabricante: {e}"

    def excluir_fabricante(self, id_fabricante) -> str:
        if not validar_id(id=id_fabricante):
            raise ValueError("Informe um código válido do fabricante")

        with Banco() as banco:
            try:
                condicao = f"id = {id_fabricante}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return f"Fabricante código {id_fabricante} excluído com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir o fabricante: {e}"

    def alterar_fabricante(self, id_fabricante, **kargs) -> str:
        if not validar_id(id=id_fabricante):
            raise ValueError("Informe um código válido do fabricante")

        with Banco() as banco:
            try:
                resultado = self.consultar_fabricante(id_fabricante=id_fabricante)

                if resultado:
                    self.nome = kargs.get("nome") or resultado[1]
                    self.site = kargs.get("site") or resultado[2]
                    valores = (self.nome, self.site)
                    condicao = f"id = {id_fabricante}"
                    banco.executar_comando("update",
                                        tabela=self.tabela,
                                        condicao=condicao,
                                        valores=valores)
                    return f"Fabricante {self.nome} alterado com sucesso."
                else:
                    return f"Não localizado fabricante com o código: {id_fabricante}"
            except RuntimeError as e:
                return f"Erro ao atualizar o fabricante: {e}"

class Cliente:

    def __init__(self, **kargs) -> None:
        self.nome = kargs.get("nome", None)
        self.endereco = kargs.get("endereco", None)
        self.telefone = kargs.get("telefone", None)
        self.email = kargs.get("email", None)
        self.id_cidade = kargs.get("id_cidade", None)
        self.tabela = "cliente"

    def consultar_cliente(self, id_cliente):
        if not validar_id(id=id_cliente):
            raise ValueError("Informe um código válido do cliente.")

        with Banco() as banco:
            try:
                condicao = f"cliente.id = {id_cliente}"
                tabela_join = ["cliente"]
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao, tabela_join=tabela_join)
                if resultado:
                    return resultado[0]
                return f"Cliente não localizado com o código {id_cliente}"
            except RuntimeError as e:
                return f"Erro ao consultar o cliente: {e}"

    def consultar_cliente_geral(self):
        with Banco() as banco:
            try:
                tabela_join = ["cliente"]
                resultado = banco.consultar(tabela=self.tabela, tabela_join=tabela_join)
                if resultado:
                    return resultado
                return "Não há clientes para serem exibidos."
            except RuntimeError as e:
                return f"Erro ao consultar os clientes: {e}"

    def cadastrar_clinte(self):
        with Banco() as banco:
            try:
                valores = (self.nome,
                            self.endereco,
                            self.telefone,
                            self.email,
                            self.id_cidade)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                return f"Cliente inserido com sucesso.\nCódigo: {novo_id}"
            except RuntimeError as e:
                return f"Erro ao inserir o cliente: {e}"

    def excluir_cliente(self, id_cliente):
        if not validar_id(id=id_cliente):
            raise ValueError("Informe um código válido do cliente.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_cliente}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return f"Cliente código {id_cliente} excluído com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir o cliente: {e}"

    def alterar_cliente(self, id_cliente, **kargs):
        if not validar_id(id=id_cliente):
            raise ValueError("Informe um código válido do cliente.")

        with Banco() as banco:
            try:
                resultado = self.consultar_cliente(id_cliente=id_cliente)
                if not resultado:
                    self.nome = kargs.get("nome") or resultado[1]
                    self.endereco = kargs.get("endereco") or resultado[2]
                    self.telefone = kargs.get("telefone") or resultado[3]
                    self.email = kargs.get("email") or resultado[4]
                    self.id_cidade = kargs.get("id_cidade") or resultado[5]
                    valores = (self.nome, self.endereco, self.telefone, self.email, self.id_cidade)
                    condicao = f"id = {id_cliente}"
                    banco.executar_comando(tipo="update",
                                        tabela=self.tabela,
                                        condicao=condicao,
                                        valores=valores)
                    return f"Cliente {self.nome} alterado com sucesso."
                else:
                    return f"Cliente não localizado com o código {id_cliente}"
            except RuntimeError as e:
                return f"Erro ao atualizar o cliente: {e}"

class Fornecedor:

    def __init__(self, **kargs) -> None:
        self.nome = kargs.get("nome", None)
        self.endereco = kargs.get("endereco", None)
        self.telefone = kargs.get("telefone", None)
        self.email = kargs.get("email", None)
        self.id_cidade = kargs.get("id_cidade", None)
        self.tabela = "fornecedor"

    def consultar_fornecedor(self, id_fornecedor):
        if not validar_id(id=id_fornecedor):
            raise ValueError("Informe um código válido do fornecedor")

        with Banco() as banco:
            try:
                condicao = f"fornecedor.id = {id_fornecedor}"
                tabela_join = ["fornecedor"]
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao, tabela_join=tabela_join)
                if resultado:
                    return resultado[0]
                return f"Fornecedor não localizado com o código {id_fornecedor}"
            except RuntimeError as e:
                return f"Erro ao consultar o fornecedor {e}"

    def consultar_fornecedor_geral(self):
        with Banco() as banco:
            try:
                tabela_join = ["fornecedor"]
                resultado = banco.consultar(tabela=self.tabela, tabela_join=tabela_join)
                if resultado:
                    return resultado
                return "Não há clientes para serem exibidos."
            except RuntimeError as e:
                return f"Erro ao consultar os fornecedores{e}"

    def cadastrar_fornecedor(self):
        with Banco() as banco:
            try:
                valores = (self.nome,
                        self.endereco,
                        self.telefone,
                        self.email,
                        self.id_cidade )
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                return f"Cliente inserido com sucesso.\nCódigo: {novo_id}"
            except RuntimeError as e:
                return f"Erro ao inserir o cliente: {e}"

    def excluir_fornecedor(self, id_fornecedor):
        if not validar_id(id=id_fornecedor):
            raise ValueError("Informe um código válido do fornecedor.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_fornecedor}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return f"Cliente código {id_fornecedor} excluído com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir o fornecedor: {e}"

    def alterar_fornecedor(self, id_forncedor, **kargs):
        if not validar_id(id=id_forncedor):
            raise ValueError("Informe um código válido do fornecedor")

        with Banco() as banco:
            try:
                resultado = self.consultar_fornecedor(id_fornecedor=id_forncedor)
                if resultado:
                    self.nome = kargs.get("nome") or resultado[1]
                    self.endereco = kargs.get("endereco") or resultado[2]
                    self.telefone = kargs.get("telefone") or resultado[3]
                    self.email = kargs.get("email") or resultado[4]
                    self.id_cidade = kargs.get("id_cidade") or resultado[5]
                    valores = (self.nome, self.endereco, self.telefone, self.email, self.id_cidade)
                    condicao = f"id = {id_forncedor}"
                    banco.executar_comando(tipo="update",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores)
                    return f"Fornecedor {self.nome} alterado com sucesso."
                else:
                    return f"Fornecedor não localizado com o código {id_forncedor}"
            except RuntimeError as e:
                return f"Erro ao alterar o fornecedor: {e}"

class Produto:

    def __init__(self, **kargs) -> None:
        self.descricao = kargs.get("descricao")
        self.estoque = 0
        self.valor_compra = 0.00
        self.valor_venda = 0.00
        self.marca = kargs.get("marca")
        self.id_fabricante = kargs.get("id_fabricante")
        self.tabela = "produto"

    def consultar_produto(self, id_produto) -> tuple:
        if not validar_id(id=id_produto):
            raise ValueError("Informe um código válido do produto.")

        with Banco() as banco:
            try:
                condicao = f"produto.id = {id_produto}"
                tabela_join = ["produto"]
                resultado = banco.consultar(tabela=self.tabela,
                                            condicao=condicao,
                                            tabela_join=tabela_join)
                if resultado:
                    return resultado[0]
                return f"Produto não localizado com o código {id_produto}"
            except RuntimeError as e:
                return f"Erro ao consultar o produto: {e}"

    def consultar_produto_geral(self) -> list[tuple]:
        with Banco() as banco:
            try:
                tabela_join = ["produto"]
                resultado = banco.consultar(tabela=self.tabela,
                                            tabela_join=tabela_join)
                if resultado:
                    return resultado
                return "Produto há produtos para serem exibidos."
            except RuntimeError as e:
                return f"Erro ao consultar os produtos: {e}"

    def cadastrar_produto(self) -> str:
        with Banco() as banco:
            try:
                valores = (self.descricao,
                        self.estoque,
                        self.valor_compra,
                        self.valor_venda,
                        self.marca,
                        self.id_fabricante)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                return f"Produto inserido com sucesso.\nCódigo: {novo_id}"
            except RuntimeError as e:
                return f"Erro ao cadastrar o produto: {e}"

    def excluir_produto(self, id_produto) -> str:
        if not validar_id(id=id_produto):
            raise ValueError("Informe um código válido do produto.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_produto}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return f"Produto código {id_produto} excluído com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir o produto: {e}"

    def alterar_produto(self, id_produto, **kargs) -> str:
        if not validar_id(id=id_produto):
            raise ValueError("Informe um código válido do produto.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_produto}"
                resultado = self.consultar_produto(id_produto=id_produto)
                if resultado:
                    self.descricao = kargs.get("descricao") or resultado[1]
                    self.estoque = kargs.get("estoque") or resultado[2]
                    self.valor_compra = kargs.get("valor_compra") or resultado[3]
                    self.valor_venda = kargs.get("valor_venda") or resultado[4]
                    self.marca = kargs.get("marca") or resultado[5]
                    self.id_fabricante = kargs.get("id_fabricante") or resultado[6]
                    valores = (self.descricao,
                               self.estoque,
                               self.valor_compra,
                               self.valor_venda,
                               self.marca,
                               self.id_fabricante)
                    condicao = f"id = {id_produto}"
                    banco.executar_comando(tipo="update",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores)
                    return f"Produto {self.descricao} alterado com sucesso."
                else:
                    return f"Não foi localizado produto com o código {id_produto}"
            except RuntimeError as e:
                return f"Erro ao atualizar o produto: {e}"

class Compra:

    def __init__(self, id_forncedor = None) -> None:
        self.id_fornecedor = id_forncedor
        self.data_compra = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.valor_total = 0.00
        self.valor_pago = 0.00
        self.desconto = 0.00
        self.finalizada = 0
        self.tabela = "compra"

    def consultar_compra(self, id_compra):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                condicao = f"compra.id = {id_compra}"
                tabela_join = ["compra"]
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao, tabela_join=tabela_join)
                if resultado:
                    return resultado[0]
                return f"Compra não localizada com o código {id_compra}"
            except RuntimeError as e:
                return f"Erro ao consultar a compra: {e}"

    def consultar_compra_geral(self):
        with Banco() as banco:
            try:
                tabela_join = ["compra"]
                resultado = banco.consultar(tabela=self.tabela, tabela_join=tabela_join)
                if resultado:
                    return resultado
                return "Não há compras para serem listadas"
            except RuntimeError as e:
                return f"Erro ao consultar a compra: {e}"

    def cadastrar_compra(self):
        with Banco() as banco:
            try:
                valores = (self.data_compra,
                        self.valor_total,
                        self.valor_pago,
                        self.desconto,
                        self.id_fornecedor,
                        self.finalizada)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                return f"Compra registrada com sucesso.\nCódigo {novo_id}", novo_id
            except RuntimeError as e:
                return f"Erro ao cadastrar a compra.{e}"

    def excluir_compra(self, id_compra):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_compra}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                return f"Compra código {id_compra} excluída com sucesso."
            except RuntimeError as e:
                return f"Erro ao excluir a compra. {e}"

    def alterar_compra(self, id_compra, **kargs):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                resultado = self.consultar_compra(id_compra=id_compra)
                if resultado:
                    self.data_compra = kargs.get("data_compra") or resultado[1]
                    self.valor_total = kargs.get("valor_total") or resultado[2]
                    self.valor_pago = kargs.get("valor_pago") or resultado[3]
                    self.desconto = kargs.get("desconto") or resultado[4]
                    self.id_fornecedor = kargs.get("id_fornecedor") or resultado[5]
                    self.finalizada = kargs.get("finalizada") or resultado[6]
                    valores = (self.data_compra,
                               self.valor_total,
                               self.valor_pago,
                               self.desconto,
                               self.id_fornecedor,
                               self.finalizada)
                    condicao = f"id = {id_compra}"
                    banco.executar_comando(tipo="update",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores)
                    return f"Compra {id_compra} atualizada com sucesso."
                else:
                    return f"Não foi localizada compra com o código {id_compra}"
            except RuntimeError as e:
                return f"Erro ao alterar o produto: {e}"

class ItemCompra:

    def __init__(self, *args) -> None:
        self.valores = args
        self.tabela = "item_compra"

    def consultar_item_compra(self, id_compra):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                condicao = f"item_compra.id_Compra = {id_compra}"
                tabela_join = ["item_compra", "produto"]
                resultado = banco.consultar(tabela=self.tabela,
                                            condicao=condicao,
                                            tabela_join=tabela_join)
                if resultado:
                    return resultado
                return f"Compra nº {id_compra} ainda não possui produtos cadastrados."
            except RuntimeError as e:
                return f"Não localizado itens com o código {e}"

    def cadastrar_item_compra(self):
        with Banco() as banco:
            try:
                #for valor in self.valores:
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=self.valores)
                return f"Item cadastrado na compra com sucesso."
            except RuntimeError as e:
                return f"Erro ao cadastrar os itens na compra: {e}"

    def excluir_item_compra(self, id_compra, produtos=()):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                condicao = f"id_compra = {id_compra} "
                if produtos:
                    condicao += f"AND id_produto in {produtos}"
                banco.executar_comando(tipo='delete', tabela=self.tabela, condicao=condicao)
                if len(produtos) > 1:
                    return f"Produtos excluídos da compra {id_compra} com sucesso"
                else:
                    return f"Produto excluído da compra {id_compra} com sucesso"
            except RuntimeError as e:
                return f"Erro ao excluir os produtos da compra: {e}"

    def alterar_item_pedido(self, id_compra, dados):
        if not validar_id(id=id_compra):
            raise ValueError("Informe um código válido da compra.")

        with Banco() as banco:
            try:
                for valor in dados:
                    condicao = f"id_compra = {id_compra} and id_produto = {valor[0]}"
                    quantidade = valor[1]
                    id_produto = valor[0]
                    id_compra = id_compra
                    valores = (quantidade, id_produto, id_compra)
                    banco.executar_comando(tipo="upate",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores)
                if len(dados) > 1:
                    return f"Itens da compra {id_compra} atualizado com sucesso."
                else:
                    return f"Item da compra {id_compra} atualizado com sucesso."
            except RuntimeError as e:
                return f"Erro ao atualizar os os produtos da  compra: {e}"

class Venda:

    def __init__(self, id_cliente = None) -> None:
        self.id_cliente = id_cliente
        self.data_venda = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.valor_total = 0.00
        self.valor_pago = 0.00
        self.valor_desconto = 0.00
        self.finalizada = 0
        self.tabela = "venda"

    def consultar_venda(self, id_venda):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_venda}"
                resultado = banco.consultar(tabela=self.tabela, condicao=condicao)
                if resultado:
                    return resultado[0]
                return f"Não foi localizado venda com o código {id_venda}"
            except RuntimeError as e:
                return f"Erro ao consultar a venda: {e}"

    def consultar_venda_geral(self):
        with Banco() as banco:
            try:
                resultado = banco.consultar(tabela=self.tabela)
                if resultado:
                    return resultado
                return "Não há vendas para serem listadas"
            except RuntimeError as e:
                return f"Erro ao consultar as vendas: {e}"

    def cadastrar_venda(self):
        with Banco() as banco:
            try:
                valores = (self.data_venda,
                        self.valor_total,
                        self.valor_pago,
                        self.valor_desconto,
                        self.id_cliente,
                        self.finalizada)
                banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valores)
                novo_id = banco.cursor.lastrowid
                print(f"Venda registrada com sucesso.\nCódigo {novo_id}")
            except RuntimeError as e:
                print(f"Erro ao registrar a venda: {e}")

    def excluir_venda(self, id_venda):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                condicao = f"id = {id_venda}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                print(f"Venda código {id_venda} excluída com sucesso.")
            except RuntimeError as e:
                print(f"Erro ao excluir a venda: {e}")

    def alterar_venda(self, id_venda, **kargs):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                resultado = self.consultar_venda(id_venda=id_venda)
                if resultado:
                    self.data_venda = kargs.get("data_venda") or resultado[1]
                    self.valor_total = kargs.get("valor_total") or resultado[2]
                    self.valor_pago = kargs.get("valor_pago") or resultado[3]
                    self.valor_desconto = kargs.get("valor_desconto") or resultado[4]
                    self.id_cliente = kargs.get("id_cliente") or resultado[5]
                    self.finalizada = kargs.get("finalizada") or resultado[6]
                    valores = (self.data_venda,
                               self.valor_total,
                               self.valor_pago,
                               self.valor_desconto,
                               self.id_cliente,
                               self.finalizada)
                    condicao = f"id = {id_venda}"
                    banco.executar_comando(tipo="update",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores
                                           )
                    print(f"Venda código {id_venda} atualizada com sucesso.")
                else:
                    print(f"Venda não localizada com o código {id_venda}")
            except RuntimeError as e:
                print(f"Erro ao alterar a venda: {e}")

class ItemVenda:

    def __init__(self, *args) -> None:
        self.valores = args
        self.tabela = "item_venda"

    def consultar_item_venda(self, id_venda):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                condicao = f"item_venda.id_venda = {id_venda}"
                tabela_join = ["item_venda"]
                resultado = banco.consultar(tabela=self.tabela,
                                            condicao=condicao,
                                            tabela_join=tabela_join)
                if resultado:
                    return resultado
                return f"Não foi localizado itens para a venda código {id_venda}"
            except RuntimeError as e:
                return f"Erro ao consultar os itens da venda: {e}"

    def cadastrar_item_venda(self):
        with Banco() as banco:
            try:
                for valor in self.valores:
                    banco.executar_comando(tipo="insert", tabela=self.tabela, valores=valor)
                if len(self.valores) > 1:
                    print(f"Itens cadastrados na compra {self.valores[0][1]} com sucesso.")
                else:
                    print(f"Item cadastrado na compra {self.valores[0][1]} com sucesso.")
            except RuntimeError as e:
                print(f"Erro ao cadastrar os itens na venda: {e}")

    def excluir_item_venda(self, id_venda, produtos=()):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                condicao = f"id_venda = {id_venda}"
                if produtos:
                    condicao += f"AND id_produto in {produtos}"
                banco.executar_comando(tipo="delete", tabela=self.tabela, condicao=condicao)
                if len(produtos) > 1:
                    print(f"Produtos excluídos da venda {id_venda} com sucesso.")
                else:
                    print(f"Produto excluído da venda {id_venda} com sucesso.")
            except RuntimeError as e:
                print(f"Erro ao exlcluir os produtos da venda: {e}")

    def alterar_item_venda(self, id_venda, dados):
        if not validar_id(id=id_venda):
            raise ValueError("Informe um código válido da venda.")

        with Banco() as banco:
            try:
                for valor in dados:
                    condicao = f"id_venda = {id_venda} and id_produto = {valor[0]}"
                    quantidade = valor[1]
                    id_produto = valor[0]
                    id_venda = id_venda
                    valores = (quantidade, id_produto, id_venda)
                    banco.executar_comando(tipo="update",
                                           tabela=self.tabela,
                                           condicao=condicao,
                                           valores=valores)
                if len(valores) > 1:
                    print(f"Produtos atualizados da venda {id_venda} com sucesso.")
                else:
                    print(f"Produto atualizado da venda {id_venda} com sucesso.")
            except RuntimeError as e:
                print(f"Erro ao atualizar os produtos da venda: {e}")
 