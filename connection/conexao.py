import sqlite3

class Banco:
    def __init__(self) -> None:
        self.nome_banco = 'connection/controleEstoque.db'
        self.conexao = None
        self.cursor = None
    
    def __enter__(self):
        try:
            self.conexao = sqlite3.connect(self.nome_banco)
            self.cursor = self.conexao.cursor()
            self.ativar_chave_estrangeira()
            return self
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao conectar ao bando de dados. Erro: {e}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_val}")
            print(f"Traceback: {exc_tb}")
        if self.conexao:
            self.conexao.close()

    def gerar_query(self, tipo, tabela, condicao=None, tabela_join = []):
        """Gera as querys dinamicamante

        Args:
            tipo (int): valor referente ao tipo da query que será gereda
                        (1 - SELECT / 2 - INSERT / 3 - DELETE / 4 - UPDATE)
            tabela (str): tabela que será utilizada na criação da query
            condicao (str, optional): Condição WHERE para utilização no SELECT, DELETE ou UPDATE. 
                                      Defaults to None.

        Raises:
            ValueError: Não foi passado o atributo condição 
            ValueError: Não foi passado o atributo condição 

        Returns:
            str: Retorna o texto com a query
        """
        sql = f"SELECT * FROM {tabela} LIMIT 1 "
        colunas = [description[0] for description in self.cursor.execute(sql).description if description[0] != 'id']
        placeholders = ', '.join('?' for _ in range(len(colunas)))
        colunas_str = ', '.join(map(str, colunas))
        join = ""
        if tabela_join:
            join = self.gerar_condicao_join(tabela_join)

        match tipo:
            case "select":
                query = f"SELECT * FROM {tabela} {join}"

                if condicao:
                    query += f"WHERE {condicao}"
                return query
            case "insert":
                return f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})"
            case "delete":
                if condicao is None:
                    raise ValueError("A condição deve ser informada para executar o DELETE.")
                return f"DELETE FROM {tabela} WHERE {condicao}"
            case "update":
                colunas_update = ", ".join([f"{coluna} = ?" for coluna in colunas if coluna != 'id'])
                if condicao is None:
                    raise ValueError("A condição é necessária para executar o UPDATE")
                return f"UPDATE {tabela} SET {colunas_update} WHERE {condicao}"
            
    def gerar_condicao_join(self, tabela_join):
        condicao_join = ''
        for tabela in tabela_join:
            query = f"PRAGMA foreign_key_list({tabela})"
            self.cursor.execute(query)
            chaves_estrangeiras = self.cursor.fetchall()
            condicao_join += "".join([f"join {valor[2]} on {valor[2]}.{valor[4]} = {tabela}.{valor[3]} " for valor in chaves_estrangeiras])
        return condicao_join

    def executar_comando(self, tipo, tabela, condicao = None, valores=()):
        try:
            sql = self.gerar_query(tipo, tabela, condicao)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            return True
        except sqlite3.Error as e:
            raise RuntimeError(f"\nErro ao executar o comando: {e}")

    def consultar(self, tabela, condicao=None, tabela_join = []):
        try:
            sql = self.gerar_query("select", tabela, condicao, tabela_join)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"\nErro ao executar a consulta: {e}")

    def ativar_chave_estrangeira(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao ativar a foreign_keys. Erro: {e}")
        
    def fechar_conexao(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexao:
                self.conexao.close()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao fechar a conexão. Erro: {e}")

