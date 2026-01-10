import sqlite3
from src.livro import Livro
import src.servico


class DataBase:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self) -> None:
        self.connection = sqlite3.connect("teste.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        _ = self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT,titulo TEXT,autor TEXT, preco REAL,ano INTEGER, quantidade INTEGER, disponivel INTEGER)"
        )
        self.connection.commit()

    def fechar(self) -> None:
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            print(f"Erro ao fechar banco! {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()

    def adicionar_livro(self, livro: Livro) -> int | None:
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
        return self.cursor.lastrowid

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

    def buscar_livros(self, coluna: str, valor: str | int) -> list[Livro]:
        if coluna not in ("titulo", "autor"):
            return []
        comando = f"SELECT * FROM livros WHERE {coluna} LIKE ?"
        sql_valor: str = f"%{valor}%"
        _ = self.cursor.execute(comando, (sql_valor,))
        encontrados = self.cursor.fetchall()
        return [Livro(*linha) for linha in encontrados]

    def gerar_relatorio(self) -> dict[str, int | str | float]:
        # Query para pegar tudo de uma vez
        comando_total = "SELECT COUNT(*) FROM livros"
        comando_disp = "SELECT COUNT(*) FROM livros WHERE disponivel = 1"
        comando_indisp = "SELECT COUNT(*) FROM livros WHERE disponivel = 0"
        comando_soma = "SELECT SUM(preco * quantidade) FROM livros"

        _ = self.cursor.execute(comando_total)
        total = self.cursor.fetchone()[0] or 0

        _ = self.cursor.execute(comando_disp)
        disp = self.cursor.fetchone()[0] or 0

        _ = self.cursor.execute(comando_indisp)
        indisp = self.cursor.fetchone()[0] or 0

        _ = self.cursor.execute(comando_soma)
        soma = self.cursor.fetchone()[0] or 0.0

        return {
            "total_livros": total,
            "livros_disponiveis": disp,
            "livros_indisponiveis": indisp,
            "valor_total_estoque": soma,
        }

    def titulo_existe(self, titulo: str) -> bool:
        comando = "SELECT 1 FROM livros WHERE LOWER(titulo) = LOWER(?) LIMIT 1"
        _ = self.cursor.execute(comando, (titulo,))
        resultado = self.cursor.fetchone()
        return resultado is not None

    def listar_id(self) -> set[int]:
        comando = "SELECT id FROM livros "
        _ = self.cursor.execute(comando)
        tuplas_id = self.cursor.fetchall()
        lista = [elemento[0] for elemento in tuplas_id]
        return set(lista)

    def buscar_por_id(self, id: int) -> list[Livro]:
        comando = "SELECT * FROM livros WHERE id = ?"
        _ = self.cursor.execute(comando, (id,))
        linha = self.cursor.fetchone()
        if linha:
            return [Livro(*linha)]
        return []
