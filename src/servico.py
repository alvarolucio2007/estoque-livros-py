from datetime import datetime

from src.database import DataBase
from src.livro import Livro


class Service:
    db: DataBase

    def __init__(self) -> None:
        self.db = DataBase()
        self.set_id = set(int(id) for id in self.db.listar_id())

    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        preco: float,
        ano: int,
        quantidade: int,
    ) -> None:
        if not titulo.strip() or not autor.strip():
            raise ValueError("Título e autor não podem ficar em branco!")
        if self.db.titulo_existe(titulo):
            raise ValueError(f"O livro {titulo} já existe!")
        if preco <= 0:
            raise ValueError("O preço tem que ser maior que 0!")
        if ano > datetime.today().year + 1:
            raise ValueError(
                f"O ano tem que ser menor que o ano atual! ({datetime.today().year + 1})"
            )
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa!")
        disponivel = 1 if quantidade > 0 else 0

        novo_livro = Livro(None, titulo, autor, preco, ano, quantidade, disponivel)
        try:
            id_gerado = self.db.adicionar_livro(novo_livro)
            if id_gerado is not None:
                self.set_id.add(id_gerado)
            else:
                raise ValueError(
                    "Erro de conexão do banco de dados! ID válido não retornado!"
                )
        except Exception as e:
            print(f"Erro crítico do banco! {e}")
            raise e

    def buscar_livro(self, tipo: str | int, valor: str) -> list[Livro]:
        if tipo == "Código":
            return self.db.buscar_por_id(int(valor))
        traducao = {"Título": "titulo", "Autor": "autor"}
        if tipo not in traducao:
            raise ValueError("O tipo de dado tem que ser ou Título, Autor, ou Código!")

        encontrados = self.db.buscar_livros(traducao[tipo], valor)
        if not encontrados:
            raise ValueError("Nenhum livro encontrado!")
        return encontrados

    def excluir_livro(self, id: int) -> None:
        if id not in self.set_id:
            raise ValueError("O id precisa existir no banco de dados!")
        self.db.deletar_livro(id)
        self.set_id.remove(id)

    def atualizar_livro(
        self, id: int, campo: str, novo_valor: str | int | float
    ) -> None:
        if id not in self.set_id:
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
            if not isinstance(novo_valor, int):
                raise ValueError(
                    "Para trocar a quantidade, é necessário que o novo valor seja um valor numérico inteiro! (Sem decimais.)"
                )
            novo_status = 1 if novo_valor > 0 else 0
            self.db.atualizar_livros(id, "disponivel", novo_status)
        self.db.atualizar_livros(id, traducao[campo], novo_valor)

    def gerar_relatorio_formatado(self) -> dict[str, int | str | float]:
        dados = self.db.gerar_relatorio()
        dados["valor_total_estoque"] = f"R$ {dados['valor_total_estoque']:.2f}"
        return dados

    def listar_todos_livros(self) -> list[Livro]:
        livros = self.db.carregar_dados()
        if not livros:
            raise ValueError("Não há livros para serem listados!")
        return livros
