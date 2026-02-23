package main

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func main() {
	// 1. Liga o banco (aquela sua função do database.go)
	ConectarBanco()

	// 2. Cria o servidor
	r := gin.Default()

	// 3. Rota de teste: Listar livros
	r.GET("/livros", func(c *gin.Context) {
		livros, err := carregarDados()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, livros)
	})
	r.GET("/atualizar", func(c *gin.Context) {
		idStr := c.Query("id")
		novoTitulo := c.Query("titulo")
		id, _ := strconv.ParseUint(idStr, 10, 32)

		// Usando aquela lógica de Update que vimos
		err := DB.Model(&Livro{}).Where("id = ?", id).Update("titulo", novoTitulo).Error
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		c.JSON(200, gin.H{"message": "Título atualizado!"})
	})
	// 4. Sobe o servidor na porta 8080
	r.Run(":8080")
}
