from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Exemplo de lista de opções para autocompletar.
opcoes = ['maçã', 'banana', 'laranja', 'pera']
completer = WordCompleter(opcoes)

fruta = prompt('Digite o nome de uma fruta: ', completer=completer)

print(f"Você escolheu: {fruta}")
