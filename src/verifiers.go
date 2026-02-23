package main

import (
	"errors"
	"fmt"
	"slices"
	"time"
)

func verificarID(id uint) bool {
	return slices.Contains(listarID(), id)
}

func servicoAdicionarLivro(titulo string, autor string, preco float64, ano int, quantidade uint) error {
	if titulo == "" {
		return errors.New("título não pode ficar em branco")
	}
	if autor == "" {
		return errors.New("autor não pode ficar em branco")
	}
	if preco <= 0 {
		return errors.New("o preço tem que ser maior que 0")
	}
	if ano > time.Now().Year()+1 {
		return fmt.Errorf("o ano %d excede o limite de lançamentos futuros (%d)", ano, time.Now().Year()+1)
	}
	disponivel := quantidade > 0

	novoLivro := Livro{
		Titulo:     titulo,
		Autor:      autor,
		Preco:      preco,
		Ano:        ano,
		Quantidade: quantidade,
		Disponivel: disponivel,
		// O ID você não precisa passar se ele for AutoIncrement

	}
	return adicionarLivro(novoLivro)
}

func servicoDeletarLivro(id uint) error {
	if id == 0 {
		return errors.New("id não pode ser 0")
	}
	return deletarLivro(id)
}

func servicoAtualizarLivro(id uint, novosDados Livro) error {
	livroExistente, err := buscarPorID(id)
	if err != nil {
		return fmt.Errorf("erro ao consultar o banco: %w", err)
	}
	if livroExistente == nil {
		return errors.New("livro não encontrado")
	}
	if novosDados.Titulo == "" {
		return errors.New("título não pode ficar vazio")
	}
	if novosDados.Preco < 0 {
		return errors.New("o preco nao pode ser negativo")
	}
	if novosDados.Ano > time.Now().Year()+1 {
		return errors.New("ano inválido")
	}
	novosDados.Disponivel = novosDados.Quantidade > 0
	err = atualizarLivro(id, novosDados)
	if err != nil {
		return fmt.Errorf("falha ao atualizar: %w", err)
	}
	return nil
}

func servicoBuscarLivroTitulo(titulo string) ([]Livro, error) {
	if titulo == "" {
		return nil, errors.New("título não pode ficar vazio")
	}
	return buscarLivroTitulo(titulo) // buscarLivroTitulo já retorna []Livro,nil então não precisa colocar nil
}

func servicoBuscarLivroAutor(autor string) ([]Livro, error) {
	if autor == "" {
		return nil, errors.New("autor não pode ficar vazio")
	}
	return buscarLivroAutor(autor) // buscarLivroAutor já retorna []Livro,nil então não precisa colocar nil
}

func servicoTituloExiste(titulo string) (bool, error) {
	if titulo == "" {
		return false, errors.New("titulo não pode ficar vazio")
	}
	return tituloExiste(titulo), nil
}

func servicoBuscarLivroId(id uint) (*Livro, error) {
	if id == 0 {
		return nil, errors.New("id não pode ser 0")
	}
	return buscarPorID(id)
}
