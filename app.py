import streamlit as st
from front.frontend import FrontEnd


def main():
    # Configurações de layout da página
    st.set_page_config(
        page_title="Sistema de Gestão de Livros", page_icon="📚", layout="wide"
    )

    # Instancia o FrontEnd (que por sua vez inicia o Service)
    app = FrontEnd()

    # Renderiza o menu e captura a escolha do usuário
    opcao = app.renderizar_menu_lateral()

    # Roteamento das páginas
    if opcao == "Cadastrar Livro":
        app.renderizar_cadastro()
    elif opcao == "Listar Livros":
        app.renderizar_listar()
    elif opcao == "Buscar Livros":
        app.renderizar_buscar()
    elif opcao == "Atualizar Livros":
        app.renderizar_atualizar()
    elif opcao == "Excluir Livros":
        app.renderizar_excluir()
    elif opcao == "Gerar Relatórios":
        app.renderizar_relatorios()


if __name__ == "__main__":
    main()
