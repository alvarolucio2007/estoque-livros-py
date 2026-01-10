import pandas as pd
import streamlit as st

import src.servico as srv


@st.cache_resource
def get_service():
    return srv.Service()


class FrontEnd:
    def __init__(self) -> None:
        self.servico = get_service()

    def exibir_mensagens_pendentes(self) -> None:
        if "success_message" in st.session_state:
            _ = st.success(st.session_state["success_message"])
            del st.session_state["success_message"]

    def renderizar_menu_lateral(self) -> str:
        with st.sidebar:
            _ = st.header("Selecione a ação")
            opcao = st.radio(
                "",
                (
                    "Cadastrar Livro",
                    "Listar Livros",
                    "Buscar Livros",
                    "Atualizar Livros",
                    "Excluir Livros",
                    "Gerar Relatórios",
                ),
            )
            return opcao

    def renderizar_cadastro(self) -> None:
        self.exibir_mensagens_pendentes()
        _ = st.markdown("Cadastro de novo livro")
        with st.form("form_cadastro"):
            titulo = st.text_input("Título do Livro", max_chars=100)
            col1, col2 = st.columns(2)
            with col1:
                autor = st.text_input("Autor do Livro", max_chars=100)
            with col2:
                ano = st.number_input(
                    "Ano de lançamento", min_value=0, format="%d", step=1
                )
            col3, col4 = st.columns(2)
            with col3:
                preco = st.number_input(
                    "Preço do Livro", min_value=0.01, format="%.2f", step=0.01
                )
            with col4:
                quantidade = st.number_input(
                    "Quantidade do Livro", min_value=0, format="%d", step=1
                )
            clique_salvar = st.form_submit_button("Cadastrar e Salvar", width="stretch")
            if clique_salvar:
                try:
                    self.servico.cadastrar_livro(
                        titulo=str(titulo),
                        preco=float(preco),
                        autor=str(autor),
                        ano=int(ano),
                        quantidade=int(quantidade),
                    )
                    st.session_state["success_message"] = (
                        f"Produto {titulo} adicionado com sucesso!"
                    )
                    st.rerun()
                except ValueError as e:
                    _ = st.error(f"Falha no cadastro! {e}")

    def renderizar_listar(self) -> None:
        _ = st.title("Visão Geral do Estoque de Livros")
        try:
            livros = self.servico.listar_todos_livros()
            if livros:
                dados_para_exibir = [vars(livro) for livro in livros]
                _ = st.dataframe(
                    dados_para_exibir, use_container_width=True, hide_index=True
                )
            else:
                _ = st.info("Nenhum livro cadastrado no momento.")
        except Exception as e:
            print(f"Erro! {e}")

    def renderizar_buscar(self) -> None:
        _ = st.markdown("Busca de Produto")
        tipo_busca = st.selectbox("Tipo de Busca", ("Código", "Título", "Autor"))
        if tipo_busca == "Código":
            busca = st.number_input("Qual seria o código?", min_value=0, step=1)
            if busca:
                resultados = self.servico.buscar_livro("Código", str(busca))
                dados = [vars(livro) for livro in resultados]
                df_resultados = pd.DataFrame(dados)
                if not df_resultados.empty:
                    _ = st.success(f"Encontrado(s) {len(df_resultados)} produto(s).")
                    _ = st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    _ = st.warning(f"Nenhum produto encontrado com o código {busca}!")
        elif tipo_busca == "Título":
            busca = st.text_input("Qual seria o título?", max_chars=100)
            if busca:
                resultados = self.servico.buscar_livro("Título", busca)
                dados = [vars(livro) for livro in resultados]
                df_resultados = pd.DataFrame(dados)
                if not df_resultados.empty:
                    _ = st.success(f"Encontrados {len(df_resultados)} produto(s).")
                    _ = st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    _ = st.warning(
                        f"Nenhum produto encontrado que inclui o título {busca}!"
                    )
        elif tipo_busca == "Autor":
            busca = st.text_input("Qual seria o autor?", max_chars=100)
            if busca:
                resultados = self.servico.buscar_livro("Autor", busca)
                dados = [vars(livro) for livro in resultados]
                df_resultados = pd.DataFrame(dados)
                if not df_resultados.empty:
                    _ = st.success(f"Encontrados {len(df_resultados)} produto(s).")
                    _ = st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    _ = st.warning(
                        f"Nenhum produto encontrado que inclui o(a) autor(a) {busca}!"
                    )

    def renderizar_atualizar(self) -> None:
        _ = st.markdown("Atualização de Produto")
        tipo_de_dado = st.selectbox(
            "Tipo de dado",
            ("Título", "Preço", "Autor", "Ano", "Quantidade"),
            key="upd_campo_select",
        )
        novo_valor = None
        with st.form("form_atualizar"):
            codigo = st.number_input("Código (ID)", min_value=1, step=1)
            if tipo_de_dado == "Preço":
                novo_valor = st.number_input(
                    "Qual seria o novo valor? ",
                    min_value=0.01,
                    step=0.01,
                    key="upd_valor_num",
                    format="%.2f",
                )
            elif tipo_de_dado in ("Título", "Autor"):
                novo_valor = st.text_input(
                    "Qual seria o novo valor? ", max_chars=100, key="upd_valor_str"
                )
            elif tipo_de_dado in ("Ano", "Quantidade"):
                novo_valor = st.number_input(
                    "Qual seria o novo valor",
                    min_value=0,
                    step=1,
                    key="upd_valor_num",
                    format="%d",
                )
            clique_salvar = st.form_submit_button("Atualizar e Salvar", width="stretch")
            if clique_salvar:
                if novo_valor is None:
                    _ = st.error("Erro! Por favor, insira o novo valor corretamente!")
                    return
                try:
                    self.servico.atualizar_livro(
                        id=int(codigo),
                        campo=tipo_de_dado,
                        novo_valor=novo_valor,
                    )
                except Exception as e:
                    _ = st.error(f"Falha na atualização: {e}!")

    def renderizar_excluir(self) -> None:
        _ = st.markdown("Excluir Livro")
        _ = st.warning("Esta ação é permanente e não pode ser desfeita!")
        self.exibir_mensagens_pendentes()
        if "codigo_excluir" not in st.session_state:
            st.session_state.codigo_excluir = None
        with st.form("form_exclusao_busca"):
            codigo_input = st.number_input("ID do livro:", min_value=1, step=1)
            botao_busca = st.form_submit_button("Buscar para exclusão")
            if botao_busca:
                st.session_state.codigo_excluir = int(codigo_input)
                st.rerun()

        if st.session_state.codigo_excluir:
            cid = st.session_state.codigo_excluir
            if cid in self.servico.set_id:
                livros = self.servico.listar_todos_livros()
                titulo = next(
                    (livro.titulo for livro in livros if livro.id == cid),
                    "Desconhecido",
                )
                _ = st.error(f"Excluir **{titulo}** (ID:{cid})?")
                if st.button("CONFIRMAR EXCLUSÃO DEFINITIVA"):
                    self.servico.excluir_livro(cid)
                    st.session_state.codigo_excluir = None  # Limpa o ID após deletar
                    st.session_state["success_message"] = f"Livro {titulo} removido!"
                    st.rerun()
        else:
            _ = st.warning("ID não encontrado no sistema.")
            st.session_state.codigo_excluir = None

    def renderizar_relatorios(self) -> None:
        _ = st.title("Relatórios de estoque dos livros")
        livros = self.servico.listar_todos_livros()
        if not livros:
            _ = st.info("Nenhum livro cadastrado para gerar relatórios.")
            return
        relatorio = self.servico.gerar_relatorio_formatado()
        col1, col2, col3, col4 = st.columns(4)
        _ = col1.metric("Total de títulos", relatorio["total_livros"])
        _ = col2.metric("Livros disponíveis", relatorio["livros_disponiveis"])
        _ = col3.metric("Livros indisponíveis", relatorio["livros_indisponiveis"])
        _ = col4.metric("Valor total do estoque", relatorio["valor_total_estoque"])
