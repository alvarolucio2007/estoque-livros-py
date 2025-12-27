import pytest
import os
from datetime import datetime
from src.servico import Service

@pytest.fixture
def service():
    if os.path.exists("teste.db"):
        os.remove("teste.db")
    s = Service()
    yield s
    s.db.connection.close()
    if os.path.exists("teste.db"):
        os.remove("teste.db")

# --- TESTES DE CADASTRO (COBRINDO VALIDAÇÕES) ---

def test_cadastrar_livro_com_sucesso(service):
    service.cadastrar_livro("O Hobbit", "Tolkien", 50.0, 1937, 10)
    assert len(service.listar_todos_livros()) == 1

def test_erro_titulo_duplicado(service):
    service.cadastrar_livro("O Hobbit", "Tolkien", 50.0, 1937, 10)
    with pytest.raises(ValueError, match="já existe"):
        service.cadastrar_livro("o hobbit", "Outro", 20.0, 2000, 1)

def test_erro_preco_invalido(service):
    with pytest.raises(ValueError, match="maior que 0"):
        service.cadastrar_livro("Livro", "Autor", 0, 2020, 1)

def test_erro_ano_futuro(service):
    ano_invalido = datetime.today().year + 2
    with pytest.raises(ValueError, match="menor que o ano atual"):
        service.cadastrar_livro("Livro", "Autor", 10.0, ano_invalido, 1)

def test_erro_quantidade_negativa(service):
    with pytest.raises(ValueError, match="não pode ser negativa"):
        service.cadastrar_livro("Livro", "Autor", 10.0, 2020, -1)

# --- TESTES DE BUSCA (COBRINDO TRADUÇÃO E ERROS) ---

def test_buscar_livro_por_titulo(service):
    service.cadastrar_livro("Pai Rico", "Kiyosaki", 40.0, 1997, 5)
    res = service.buscar_livro("Título", "Pai")
    assert res[0].titulo == "Pai Rico"

def test_buscar_livro_por_autor(service):
    service.cadastrar_livro("Livro X", "Machado de Assis", 30.0, 1880, 2)
    res = service.buscar_livro("Autor", "Machado")
    assert res[0].autor == "Machado de Assis"

def test_erro_tipo_busca_invalido(service):
    with pytest.raises(ValueError, match="ou Título ou Autor"):
        service.buscar_livro("Preço", "10")

def test_erro_nenhum_livro_encontrado(service):
    with pytest.raises(ValueError, match="Nenhum livro encontrado"):
        service.buscar_livro("Título", "Inexistente")

# --- TESTES DE EXCLUSÃO ---

def test_excluir_livro_com_sucesso(service):
    service.cadastrar_livro("Excluir", "Autor", 10.0, 2000, 1)
    service.excluir_livro(1)
    with pytest.raises(ValueError, match="Não há livros"):
        service.listar_todos_livros()

def test_erro_excluir_id_inexistente(service):
    with pytest.raises(ValueError, match="precisa existir"):
        service.excluir_livro(999)

# --- TESTES DE ATUALIZAÇÃO (O GRANDE VILÃO DA COBERTURA) ---

def test_atualizar_campos_string(service):
    service.cadastrar_livro("Antigo", "Antigo", 10.0, 2000, 1)
    service.atualizar_livro(1, "Título", "Novo Título")
    service.atualizar_livro(1, "Autor", "Novo Autor")
    livro = service.listar_todos_livros()[0]
    assert livro.titulo == "Novo Título"
    assert livro.autor == "Novo Autor"

def test_atualizar_campos_numericos(service):
    service.cadastrar_livro("Livro", "Autor", 10.0, 2000, 10)
    service.atualizar_livro(1, "Preço", 99.9)
    service.atualizar_livro(1, "Ano", 2022)
    service.atualizar_livro(1, "Quantidade", 5)
    livro = service.listar_todos_livros()[0]
    assert livro.preco == 99.9
    assert livro.ano == 2022
    assert livro.quantidade == 5

def test_erro_atualizar_id_inexistente(service):
    with pytest.raises(ValueError, match="precisa existir"):
        service.atualizar_livro(999, "Título", "Erro")

def test_erro_atualizar_campo_invalido(service):
    service.cadastrar_livro("Livro", "Autor", 10.0, 2000, 10)
    with pytest.raises(ValueError, match="uma das opções"):
        service.atualizar_livro(1, "Editora", "Erro")

def test_erro_tipo_dado_errado_atualizacao(service):
    service.cadastrar_livro("Livro", "Autor", 10.0, 2000, 10)
    # Título deve ser string
    with pytest.raises(ValueError, match="necessário que o novo valor seja texto"):
        service.atualizar_livro(1, "Título", 123)
    # Preço deve ser float
    with pytest.raises(ValueError, match="valor numérico com decimais"):
        service.atualizar_livro(1, "Preço", "caro")
    # Quantidade deve ser int
    with pytest.raises(ValueError, match="valor numérico inteiro"):
        service.atualizar_livro(1, "Quantidade", 10.5)

# --- RELATÓRIO E LISTAGEM ---

def test_gerar_relatorio_formatado(service):
    service.cadastrar_livro("A", "Aut", 10.0, 2000, 2)
    rel = service.gerar_relatorio_formatado()
    assert rel["Soma: "] == "R$ 20.00"

def test_listar_todos_vazio_erro(service):
    with pytest.raises(ValueError, match="Não há livros"):
        service.listar_todos_livros()