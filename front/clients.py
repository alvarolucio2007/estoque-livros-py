import requests

API_URL = "http://127.0.0.1:8000"


def _tratar_resposta(response):
    """Função auxiliar para validar o status code e tratar erros."""
    if response.status_code == 200 or response.status_code == 201:
        return response.json()

    # Se chegou aqui, deu erro
    try:
        detalhe = response.json().get("detail", "Erro desconhecido")
    except ValueError:
        detalhe = response.text

    raise Exception(f"Falha na API ({response.status_code}): {detalhe}")


def listar_livro():
    try:
        # Tenta bater na porta da API
        response = requests.get(
            f"{API_URL}/livros", timeout=10
        )  # Timeout é bom pra não travar o app pra sempre
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        # Se ninguém atender a porta (API desligada/Rede caiu)
        raise Exception("Erro de Conexão: A API parece estar offline ou inalcançável.")
    except requests.exceptions.Timeout:
        raise Exception("Erro de Tempo: A API demorou demais para responder.")


def gerar_relatorio():
    try:
        response = requests.get(f"{API_URL}/livros/relatorio", timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão: A API parece estar offline ou inalcançável.")
    except requests.exceptions.Timeout:
        raise Exception("Erro de Tempo: A API demorou demais para responder.")


def cadastrar_livro(livro_dados: dict):
    try:
        response = requests.post(f"{API_URL}/livros", json=livro_dados, timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar cadastrar.")


def deletar_livro(livro_id: int):
    try:
        response = requests.delete(f"{API_URL}/livros/{livro_id}", timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão ao tentar deletar.")


def buscar_livro(livro_id: int):
    try:
        response = requests.get(f"{API_URL}/livros/{livro_id}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar buscar o livro. ")


def editar_titulo(livro_id: int, titulo: str):
    try:
        response = requests.get(f"{API_URL}/livros/{livro_id}/titulo?titulo={titulo}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar editar o título.")


def editar_autor(livro_id: int, autor: str):
    try:
        response = requests.get(f"{API_URL}/livros/{livro_id}/autor?autor={autor}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar editar o título.")


def editar_quantidade(livro_id: int, quantidade: int):
    try:
        response = requests.get(
            f"{API_URL}/livros/{livro_id}/titulo?titulo={quantidade}"
        )
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar editar o título.")
