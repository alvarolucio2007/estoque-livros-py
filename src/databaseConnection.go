package main

import (
	"errors"
	"fmt"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConectarBanco() {
	dsn := "host=localhost user=user_projeto password=password_projeto dbname=db_estoque port=5432 sslmode=disable"
	var err error
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Não foi possível conectar ao Postgres! ", err)
	}
	fmt.Println("Banco conectado com sucesso!")
	err = DB.AutoMigrate(&Livro{})
	if err != nil {
		log.Fatal("Erro interno no servidor!", err)
	}
}

func (l *Livro) AntesSalvar(tx *gorm.DB) (err error) {
	l.Disponivel = l.Quantidade > 0
	return nil
}

func checarResultado(resultado *gorm.DB) error {
	if resultado.Error != nil {
		return resultado.Error
	}
	if resultado.RowsAffected == 0 {
		return errors.New("nenhum livro encontrado com esse ID")
	}
	return nil
}

func adicionarLivro(dados Livro) error {
	resultado := DB.Create(&dados)
	if resultado.Error != nil {
		return resultado.Error
	}
	return nil
}

func carregarDados() ([]Livro, error) {
	var livros []Livro
	resultado := DB.Find(&livros)
	if resultado.Error != nil {
		return nil, resultado.Error
	}
	return livros, nil
}

func deletarLivro(id uint) error {
	return checarResultado(DB.Delete(&Livro{}, id))
}

func atualizarLivro(id uint, dados Livro) error {
	return checarResultado(DB.Model(&Livro{}).Where("id=?", id).Updates(dados))
}

func buscarLivroTitulo(titulo string) ([]Livro, error) {
	var livrosEncontados []Livro
	res := DB.Where("titulo LIKE ?", "%"+titulo+"%").Find(&livrosEncontados)
	err := checarResultado(res)
	if err != nil {
		return nil, err
	}
	return livrosEncontados, nil
}

func buscarLivroAutor(autor string) ([]Livro, error) {
	var livrosEncontados []Livro
	res := DB.Where("autor LIKE ?", "%"+autor+"%").Find(&livrosEncontados)
	err := checarResultado(res)
	if err != nil {
		return nil, err
	}
	return livrosEncontados, nil
}

func gerarRelatorio() (map[string]any, error) {
	var total, disponiveis, indisponiveis int64
	var valorTotal float64
	DB.Model(&Livro{}).Count(&total)
	DB.Model(&Livro{}).Where("disponivel=?", true).Count(&disponiveis)
	DB.Model(&Livro{}).Where("disponivel=?", false).Count(&indisponiveis)
	DB.Model(&Livro{}).Select("SUM(preco*quantidade)").Scan(&valorTotal)
	return map[string]any{
		"total_livros":         total,
		"livros_disponiveis":   disponiveis,
		"livros_indisponiveis": indisponiveis,
		"valor_total_estoque":  valorTotal,
	}, nil
}

func tituloExiste(titulo string) bool {
	var existe bool
	err := DB.Model(&Livro{}).Select("count(*)>0").Where("Lower(titulo)=LOWER(?)", titulo).Find(&existe).Error
	if err != nil {
		return false
	}
	return existe
}

func listarID() []uint {
	var livros []Livro
	DB.Find(&livros)
	setIds := make(map[uint]struct{})
	for _, livro := range livros {
		setIds[uint(livro.ID)] = struct{}{}
	}
	idUnicos := make([]uint, 0, len(setIds))
	for id := range setIds {
		idUnicos = append(idUnicos, id)
	}
	return idUnicos
}

func buscarPorID(id uint) (*Livro, error) {
	var livro Livro
	if err := DB.First(&livro, id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return &livro, nil
}
