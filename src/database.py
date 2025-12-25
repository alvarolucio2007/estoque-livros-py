import sqlite3
from src.livro import Livro


class DataBase:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self) -> None:
        self.connection = sqlite3.connect("teste.db")
        self.cursor = self.connection.cursor()
        _ = self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT,titulo TEXT,autor TEXT, preco REAL,ano INTEGER, quantidade INTEGER, disponivel INTEGER)"
        )
        self.connection.commit()

    def adicionar_livro(self, livro: Livro) -> None:
        comando = "INSERT INTO livros (titulo,autor,preco,ano,quantidade,disponivel) VALUES (?,?,?,?,?,?)"
        dados = (
            livro.titulo,
            livro.autor,
            livro.preco,
            livro.ano,
            livro.quantidade,
            livro.disponivel,
        )
        _ = self.cursor.execute(comando, dados)
        self.connection.commit()

    def carregar_dados(self) -> list[Livro]:
        comando = "SELECT * FROM livros"
        _ = self.cursor.execute(comando)
        linhas = self.cursor.fetchall()
        lista_livros: list[Livro] = [Livro(*linha) for linha in linhas]
        return lista_livros

    def deletar_dados(self, id: int) -> None:
        id_tupla = (id,)
        comando = "DELETE FROM livros WHERE id = ?"
        _ = self.cursor.execute(comando, id_tupla)
        self.connection.commit()

    def atualizar_dados(
        self, id: int, campo: str, novo_valor: str | int | float
    ) -> None:
        if campo not in ("titulo", "autor", "preco", "ano", "quantidade"):
            return None
        if campo == "quantidade" and isinstance(novo_valor, int):
            comando = f"UPDATE livros SET {campo} = ?, disponivel = ? WHERE id = ? "
            disponivel = 1 if novo_valor > 0 else 0
            _ = self.cursor.execute(comando, (novo_valor, disponivel, id))
        else:
            comando = f"UPDATE livros SET {campo} = ? WHERE id = ?"
            _ = self.cursor.execute(comando, (novo_valor, id))
        self.connection.commit()
