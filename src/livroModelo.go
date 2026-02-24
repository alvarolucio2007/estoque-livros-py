package main

type Livro struct {
	ID         uint    `json:"id" gorm:"primaryKey;autoIncrement"`
	Titulo     string  `json:"titulo" gorm:"not null"`
	Autor      string  `json:"autor" gorm:"not null"`
	Preco      float64 `json:"preco" gorm:"type:decimal(10,2)"`
	Ano        int     `json:"ano"`
	Quantidade uint    `json:"quantidade"`
	Disponivel bool    `json:"disponivel" gorm:"default:true"`
}
type LivroCadastrar struct {
	Titulo     string  `json:"titulo" gorm:"not null"`
	Autor      string  `json:"autor" gorm:"not null"`
	Preco      float64 `json:"preco" gorm:"type:decimal(10,2)"`
	Ano        int     `json:"ano"`
	Quantidade uint    `json:"quantidade"`
}
