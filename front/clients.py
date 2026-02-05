import requests

API_URL = "http://127.0.0.1:8000"


def listar_livro():
    url_get = f"{API_URL}/livros"
    try:
        response = requests.get(url_get)
        if response.status_code == 200:
            livros = response.json()
            return livros
        elif response.status_code == 404:
            raise Exception("Livro não encontrado no banco de dados!")
        else:
            raise Exception(f"Erro na API: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Não foi possível se conectar à API. Verifique se o FastAPI está funcionando!"
        )
