from datetime import datetime
from database import DataBase
from livro import Livro


class Service:
    db: DataBase

    def __init__(self) -> None:
        self.db = DataBase()
        self.set_id = set(int(id) for id in self.db.listar_id())

    def verificar_id(self, id: int) -> None | bool:
        if id not in self.set_id:
            return None
        return True

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

        novo_livro = Livro(
            id=None,
            titulo=titulo,
            autor=autor,
            preco=preco,
            ano=ano,
            quantidade=quantidade,
            disponivel=disponivel,
        )
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

    def buscar_livro(self, tipo: str | int, valor: str) -> list[Livro] | Livro | None:
        if tipo == "Código":
            return self.db.buscar_por_id(int(valor))
        traducao = {"Título": "titulo", "Autor": "autor"}
        if tipo not in traducao:
            raise ValueError("O tipo de dado tem que ser ou Título, Autor, ou Código!")

        encontrados = self.db.buscar_livros(traducao[tipo], valor)
        if not encontrados:
            raise ValueError("Nenhum livro encontrado!")
        return encontrados

    def buscar_livro_codigo(self, id: int) -> Livro | None:
        if not self.verificar_id(id):
            return None
        encontrados = self.db.buscar_por_id(int(id))
        if not encontrados:
            raise ValueError("Nenhum livro encontrado!")
        return encontrados

    def buscar_livro_titulo(self, titulo: str) -> list[Livro] | None:
        encontrados = self.db.buscar_livros("titulo", titulo)
        if not encontrados:
            raise ValueError("Nenhum Livro Encontrado!")
        return encontrados

    def buscar_livro_autor(self, autor: str) -> list[Livro]:
        encontrados = self.db.buscar_livros("autor", autor)
        if not encontrados:
            raise ValueError("Nenhum Livro Encontrado!")
        return encontrados

    def excluir_livro(self, id: int) -> None | bool:
        if not self.verificar_id(id):
            return None
        self.db.deletar_livro(id)
        self.set_id.remove(id)
        return True

    def atualizar_livro(
        self, id: int, campo: str, novo_valor: str | int | float
    ) -> None:
        if not self.verificar_id(id):
            return None
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

    def atualizar_livro_titulo(self, id: int, novo_titulo: str) -> Livro | None:
        if not self.verificar_id(id):
            return None
        self.db.atualizar_livros(id, "titulo", novo_titulo)
        return self.db.buscar_por_id(id)

    def atualizar_livro_autor(self, id: int, novo_autor: str) -> Livro | None:
        if not self.verificar_id(id):
            return None
        self.db.atualizar_livros(id, "autor", novo_autor)
        return self.db.buscar_por_id(id)

    def atualizar_livro_ano(self, id: int, novo_ano: int) -> Livro | None:
        if not self.verificar_id(id):
            return None
        self.db.atualizar_livros(id, "ano", novo_ano)
        return self.db.buscar_por_id(id)

    def atualizar_livro_quantidade(self, id: int, novo_quantidade: int) -> Livro | None:
        if not self.verificar_id(id):
            return None
        self.db.atualizar_livros(id, "quantidade", novo_quantidade)
        return self.db.buscar_por_id(id)

    def atualizar_livro_preco(self, id: int, preco: float) -> Livro | None:
        if not self.verificar_id(id):
            return None
        self.db.atualizar_livros(id, "preco", preco)
        return self.db.buscar_por_id(id)

    def gerar_relatorio_formatado(self) -> dict[str, int | str | float]:
        dados = self.db.gerar_relatorio()
        dados["valor_total_estoque"] = f"R$ {dados['valor_total_estoque']:.2f}"
        return dados

    def listar_todos_livros(self) -> list[Livro]:
        livros = self.db.carregar_dados()
        if not livros:
            raise ValueError("Não há livros para serem listados!")
        return livros
