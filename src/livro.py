from pydantic import BaseModel


class Livro(BaseModel):
    id: int | None = None
    titulo: str
    autor: str
    preco: float
    ano: int
    quantidade: int
    disponivel: bool | int


class LivroCadastrar(BaseModel):
    titulo: str
    autor: str
    preco: float
    ano: int
    quantidade: int
