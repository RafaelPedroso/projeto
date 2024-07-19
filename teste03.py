import questionary

questoes = questionary.form(
    primeira = questionary.text("Digite o 1º: "),
    sequnda = questionary.text("Digite o 2º: "),
    terceira = questionary.text("Digite o 3º: "),
)

from tabulate import tabulate

dados = [(1152, 'Nova cidade', 'SP')]

print(tabulate(dados, headers=["id","nome","uf"]))