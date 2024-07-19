from prompt_toolkit.document import Document
from questionary import Validator, ValidationError, Style
import os

class ValidadorValorNulo(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message=f"Por favor digitar o valor.",
                cursor_position=len(document.text),
            )

class ValidadorNumero(Validator):
    def validate(self, document: Document):
        texto = document.text
        if not texto.isdigit():
            raise ValidationError(
                message="Entrada inválida: apenas números são permitidos.",
                cursor_position=len(texto))

class ValidarAutoComplete(Validator):
    def __init__(self, lista:list) -> None:
        self.__lista = lista

    def validate(self, document: Document) -> None:
        texto = document.text
        ok = texto in self.__lista
        if len(texto) == 0 or not ok:
            raise ValidationError(
                message="Escolha uma cidade válida.",
                cursor_position=len(texto))
        
class ValidarItemInserido(Validator):
    def __init__(self, nomes_produtos: list, produtos_inserido) -> None:
        self.__nomes_produtos = nomes_produtos
        self.__produtos_inseridos = produtos_inserido

    def validate(self, document: Document) -> None:
        texto = document.text
        produto_existe = texto in self.__nomes_produtos
        produto_ja_inserido = texto in self.__produtos_inseridos
        if produto_ja_inserido:
            raise ValidationError(message="Produto já cadastrado.",
                                  cursor_position=len(texto))
        elif len(texto) == 0 or not produto_existe:
            raise ValidationError(message="Escolha um produto válido.",
                                  cursor_position=len(texto))

class ValidarOpcao(Validator):
    def __init__(self, opcoes: list) -> None:
        self.__opcoes = opcoes
    
    def validate(self, document: Document) -> None:
        texto = document.text
        if len(texto) ==0 or texto not in self.__opcoes:
            raise ValidationError(
                message="Escolha uma opção valida.",
                cursor_position=len(texto)
            )

def validar_id(id):
    if id is None or not isinstance(id, int) or id <= 0:
        return False
    return True

def limpar_tela() ->None:
    """Limpa tela do programa
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def estilo_questionary():
    estilo = Style([
        ('qmark', '#fac731 bold'),        # Marca de pergunta
        ('question', 'bold yellow'),      # Texto da pergunta
        ('answer', '#f2c811 bold'),       # Texto da resposta
        ('pointer', 'bold #673ab7'),      # Ponteiro de seleção
        ('highlighted', '#34acdf'),       # Texto destacado
        ('selected', '#0abf5b'),          # Texto selecionado
        ('separator', '#cc5454'),         # Separador de seções
        ('instruction', 'italic'),        # Instruções
        ('text', 'default'),              # Texto padrão
        ('disabled', '#858585 italic'),    # Texto desabilitado
    ])
    return estilo

def estilo_print():
    return 'bold italic fg:darkred'

def cabecalho():
    
    limpar_tela()

    print(f"{'='*50}")
    print(f"{'Gerenciamento de estoque':^50}")
    print(f"{'='*50}")