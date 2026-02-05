from fastapi import FastAPI, Depends, HTTPException
from servico import Service
from livro import LivroCadastrar

app = FastAPI()


@app.get("/livros")
async def listar_livros(service: Service = Depends(Service)):
    return service.listar_todos_livros()


@app.get("/livros/relatorio")
async def gerar_relatorio(service: Service = Depends(Service)):
    return service.gerar_relatorio_formatado()


@app.get("/livros/{livro_id}", status_code=200)
async def buscar_livro(livro_id: int, service: Service = Depends(Service)):
    busca = service.buscar_livro_codigo(livro_id)
    if not busca:
        raise HTTPException(status_code=404, detail="Livro Não Encontrado!")
    return busca


@app.post("/livros", status_code=201)
async def cadastrar_livro(livro: LivroCadastrar, service: Service = Depends(Service)):
    try:
        service.cadastrar_livro(**livro.model_dump())
        return {"mensagem": "Livro Cadastrado com sucesso!", "livro": livro}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/livros/{id}/titulo")
async def editar_titulo(id: int, titulo: str, service: Service = Depends(Service)):
    livro_atualizado = service.atualizar_livro_titulo(id, titulo)
    if livro_atualizado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
    return livro_atualizado


@app.patch("/livros/{id}/autor")
async def editar_autor(id: int, autor: str, service: Service = Depends(Service)):
    livro_atualizado = service.atualizar_livro_autor(id, autor)
    if livro_atualizado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
    return livro_atualizado


@app.patch("/livros/{id}/quantidade")
async def editar_quantidade(
    id: int, quantidade: int, service: Service = Depends(Service)
):
    livro_atualizado = service.atualizar_livro_quantidade(id, quantidade)
    if livro_atualizado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
    return livro_atualizado


@app.patch("/livros/{id}/ano")
async def editar_ano(id: int, ano: int, service: Service = Depends(Service)):
    livro_atualizado = service.atualizar_livro_ano(id, ano)
    if livro_atualizado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
    return livro_atualizado


@app.patch("/livros/{id}/preco")
async def editar_preco(id: int, preco: float, service: Service = Depends(Service)):
    livro_atualizado = service.atualizar_livro_preco(id, preco)
    if livro_atualizado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")

    return livro_atualizado


@app.delete("/livros/{id}")
async def deletar_livro(id: int, service: Service = Depends(Service)):
    livro_deletado = service.excluir_livro(id)
    if livro_deletado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
