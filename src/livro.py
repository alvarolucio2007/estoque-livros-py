import dataclasses


@dataclasses.dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    preco: float
    ano: int
    quantidade: int
    disponivel: bool
