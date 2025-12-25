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

    def deletar_livro(self, id: int) -> None:
        id_tupla = (id,)
        comando = "DELETE FROM livros WHERE id = ?"
        _ = self.cursor.execute(comando, id_tupla)
        self.connection.commit()

    def atualizar_livros(
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

    def listar_livros(self) -> list[Livro]:
        return self.carregar_dados()

    def buscar_livros(self, coluna: str, valor: str | int) -> list[Livro]:
        if coluna not in ("titulo", "autor"):
            return []
        comando = f"SELECT * FROM livros WHERE {coluna} LIKE ?"
        sql_valor: str = f"%{valor}%"
        _ = self.cursor.execute(comando, (sql_valor,))
        encontrados = self.cursor.fetchall()
        return [Livro(*linha) for linha in encontrados]

    def gerar_relatorio(self) -> dict[str, int | str | float]:
        comando = (
            "SELECT COUNT(*), SUM(preco * quantidade), SUM(quantidade) FROM livros"
        )
        _ = self.cursor.execute(comando)
        tupla: tuple[str, float | None, int | None] = self.cursor.fetchone()
        return {
            "Títulos: ": tupla[0],
            "Soma: ": tupla[1] or 0.0,
            "Estoque utilizado: ": tupla[2] or 0,
        }

    def titulo_existe(self, titulo: str) -> bool:
        comando = "SELECT 1 FROM livros WHERE LOWER(titulo) = LOWER(?) LIMIT 1"
        _ = self.cursor.execute(comando, (titulo,))
        resultado = self.cursor.fetchone()
        return resultado is not None
