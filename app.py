import questionary
from auxiliar import limpar_tela, estilo_questionary
from controller.cidade import cidade
from controller.fabricante import fabricante
from controller.cliente import cliente
from controller.fornecedor import fornecedor
from controller.produto import produto
from controller.compra import compra


def menu_principal():
    opcoes = [
        {"name":"  Cadastros", "value":"1"},
        {"name":"  Movimentos", "value":'2'},
        {"name":"  Consultas", "value":"3"},
        questionary.Separator(),
        {"name":"  Sair", "value":"4"},
    ]

    selecao = questionary.select("Menu principal",
                                 choices=opcoes,
                                 instruction=" ",
                                 qmark=" ",
                                 style=estilo_questionary(),).ask()

    return selecao

def submenu_cadastro():
    opcoes = [
        {"name":"  Cidade", "value":"1"},
        {"name":"  Fabricante", "value":"2"},
        {"name":"  Cliente", "value":"3"},
        {"name":"  Fornecedor", "value":"4"},
        {"name":"  Produto", "value":"5"},
        questionary.Separator(),
        {"name":"  Voltar", "value":"6"},
    ]

    selecao = questionary.select("Cadastro",
                                 choices=opcoes,
                                 instruction=" ",
                                 qmark=" ",
                                 style=estilo_questionary(),).ask()

    return selecao

def submenu_movimentos():
    opcoes = [
        {"name":"  Compras", "value":"1"},
        {"name":"  Vendas", "value":"2"},        
        questionary.Separator(),
        {"name":"  Voltar", "value":"3"},
    ]

    selecao = questionary.select("Movimentos",
                                 choices=opcoes,
                                 instruction=" ",
                                 qmark=" ",
                                 style=estilo_questionary(),).ask()

    return selecao

def main():

    while True:

        limpar_tela()

        print(f"{'='*50}")
        print(f"{'Gerenciamento de estoque':^50}")
        print(f"{'='*50}")

        opcao = menu_principal()

        match opcao:
            case "1":
                while True:
                    limpar_tela()
                    print(f"{'='*50}")
                    print(f"{'Gerenciamento de estoque':^50}")
                    print(f"{'='*50}")
                    selecao_submenu = submenu_cadastro()
                    match selecao_submenu:
                        case "1":
                            cidade()
                        case "2":
                            fabricante()
                        case "3":
                            cliente()
                        case "4":
                            fornecedor()
                        case "5":
                            produto()
                        case "6":
                            break                
            case "2":
                limpar_tela()
                selecao_submenu = submenu_movimentos()
                match selecao_submenu:
                    case "1":
                        compra()
                    case "2":
                        print("vendas")
                    case "3":
                        break
            case "3":
                pass
            case "4":
                break

if __name__=="__main__":
    main()
