import requests
import os


API_URL = os.getenv("API_URL", "http://localhost:8000")


def _tratar_resposta(response):
    """Função auxiliar para validar o status code e tratar erros."""
    if response.status_code in [200, 201]:  # 200: OK, 201: Created
        return response.json()
    # Se chegou aqui, deu erro
    try:
        err_json = response.json()
        mensagem = (
            response.get("detail") or err_json.get("mensagem") or "Erro desconhecido"
        )
    except Exception:
        mensagem = f"Erro no servidor: {response.status_code}"
    raise ValueError(mensagem)


# --- GET (Ler) ---


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


def listar_id():
    try:
        response = requests.get(f"{API_URL}/livros/listar_id", timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão: A API parece estar offline ou inalcançável.")
    except requests.exceptions.Timeout:
        raise Exception("Erro de Tempo: A API demorou demais para responder.")


def buscar_livro_codigo(livro_id: int):
    try:
        response = requests.get(f"{API_URL}/livros/{livro_id}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar buscar o livro. ")


def buscar_livro_autor(autor: str):
    try:
        response = requests.get(f"{API_URL}/livros/autor/{autor}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar buscar o livro. ")


def buscar_livro_titulo(titulo: str):
    try:
        response = requests.get(f"{API_URL}/livros/titulo/{titulo}")
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar buscar o livro. ")


# --- POST (Criar) ---


def cadastrar_livro(livro_dados: dict):
    try:
        response = requests.post(f"{API_URL}/livros", json=livro_dados, timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar cadastrar")


# --- Put (Editar) ---


def editar_livro(livro_dados: dict, id: int):
    try:
        response = requests.put(f"{API_URL}/livros/{id}", json=livro_dados, timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão ao tentar editar")


# --- Delete (Remover) ---
def deletar_livro(livro_id: int):
    try:
        response = requests.delete(f"{API_URL}/livros/{livro_id}", timeout=10)
        return _tratar_resposta(response)
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão ao tentar deletar.")
