from datetime import datetime

from src.database import DataBase
from src.livro import Livro


class Service:
    db: DataBase

    def __init__(self) -> None:
        self.db = DataBase()

    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        preco: float,
        ano: int,
        quantidade: int,
    ) -> None:
        if self.db.titulo_existe(titulo):
            raise ValueError(f"O livro {titulo} já existe!")
        if preco <= 0:
            raise ValueError("O preço tem que ser maior que 0!")
        if ano > datetime.today().year + 1:
            raise ValueError(
                f"O ano tem que ser menor que o ano atual! ({datetime.today().year + 1})"
            )
        if quantidade<0:
            raise ValueError("A quantidade não pode ser negativa!")
        disponivel = 1 if quantidade > 0 else 0

        novo_livro = Livro(None, titulo, autor, preco, ano, quantidade, disponivel)
        self.db.adicionar_livro(novo_livro)

    def buscar_livro(self, tipo: str, valor: str) -> list[Livro]:
        traducao = {"Título": "titulo", "Autor": "autor"}
        if tipo not in traducao:
            raise ValueError("O tipo de dado tem que ser ou Título ou Autor!")
        coluna_sql = traducao[tipo]
        encontrados = self.db.buscar_livros(coluna_sql, valor)
        if not encontrados:
            raise ValueError("Nenhum livro encontrado!")
        return encontrados

    def excluir_livro(self, id: int) -> None:
        set_ids = self.db.listar_id()
        if id not in set_ids:
            raise ValueError("O id precisa existir no banco de dados!")
        self.db.deletar_livro(id)

    def atualizar_livro(
        self, id: int, campo: str, novo_valor: str | int | float
    ) -> None:
        set_ids = self.db.listar_id()
        if id not in set_ids:
            raise ValueError("O id precisa existir no banco de dados!")
        traducao = {
            "Título": "titulo",
            "Autor": "autor",
            "Preço": "preco",
            "Ano": "ano",
            "Quantidade": "quantidade",
        }
        if campo not in traducao:
            raise ValueError(f"O campo precisa ser uma das opções: {traducao.keys()}")
        if campo in ("Título", "Autor") and not isinstance(novo_valor, str):
            raise ValueError(
                "Para trocar o título ou autor, é necessário que o novo valor seja texto!"
            )
        if campo == "Preço" and not isinstance(novo_valor, float):
            raise ValueError(
                "Para trocar o preço, é necessário que o novo valor seja um valor numérico com decimais! "
            )
        if campo == "Quantidade" and not isinstance(novo_valor, int):
            raise ValueError(
                "Para trocar a quantidade, é necessário que o novo valor seja um valor numérico inteiro! (Sem decimais.)"
            )
        self.db.atualizar_livros(id, traducao[campo], novo_valor)

    def gerar_relatorio_formatado(self) -> dict[str, int | str | float]:
        dados = self.db.gerar_relatorio()
        dados["Soma: "] = f"R$ {dados['Soma: ']:.2f}"
        return dados

    def listar_todos_livros(self) -> list[Livro]:
        livros = self.db.carregar_dados()
        if not livros:
            raise ValueError("Não há livros para serem listados!")
        return livros
