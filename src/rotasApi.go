package main

import (
	"strconv"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func setupAPI() {
	r := gin.Default()
	config := cors.Config{
		AllowOrigins:     []string{"http://localhost:8501"},
		AllowMethods:     []string{"GET", "POST", "PATCH", "DELETE", "PUT"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		AllowCredentials: true,
	}
	r.Use(cors.New(config))

	r.GET("/livros", func(c *gin.Context) {
		livros, err := carregarDados()
		if err != nil {
			c.JSON(500, gin.H{"error": "Erro ao ler banco de dados"})
			return
		}
		c.JSON(200, livros)
	})
	r.GET("/livros/listar_id", func(c *gin.Context) {
		resultado := listarID()
		c.JSON(200, resultado)
	})
	r.GET("/livros/relatorio", func(c *gin.Context) {
		resultado, err := gerarRelatorio()
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao gerar relatorio"})
			return
		}
		c.JSON(200, resultado)
	})
	r.GET("/livros/:livro_id", func(c *gin.Context) {
		idStr := c.Param("livro_id")
		idUint, err := strconv.ParseUint(idStr, 10, 64)
		if err != nil {
			c.JSON(400, gin.H{"error": "o id deve ser um número válido"})
		}
		resultado, err := servicoBuscarLivroId(uint(idUint))
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao procurar livro por id"})
			return
		}
		c.JSON(200, resultado)
	})
	r.GET("/livros/titulo/:titulo", func(c *gin.Context) {
		tituloStr := c.Param("titulo")
		resultado, err := servicoBuscarLivroTitulo(tituloStr)
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao procurar livro por título"})
			return
		}
		c.JSON(200, resultado)
	})
	r.GET("/livros/autor/:autor", func(c *gin.Context) {
		tituloStr := c.Param("autor")
		resultado, err := servicoBuscarLivroTitulo(tituloStr)
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao procurar livro por autor"})
			return
		}
		c.JSON(200, resultado)
	})
	r.POST("/livros", func(c *gin.Context) {
		var novoLivro LivroCadastrar
		if err := c.ShouldBindJSON(&novoLivro); err != nil {
			c.JSON(400, gin.H{"error": "JSON inválido: " + err.Error()})
			return
		}
		err := servicoAdicionarLivro(novoLivro.Titulo, novoLivro.Autor, novoLivro.Preco, novoLivro.Ano, novoLivro.Quantidade)
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao salvar no banco"})
			return
		}
		c.JSON(201, "criado com sucesso")
	})
	r.PUT("/livros/:id/", func(c *gin.Context) {
		idStr := c.Param("id")
		idUint, err := strconv.ParseUint(idStr, 10, 64)
		if err != nil {
			c.JSON(400, gin.H{"error": "o id deve ser um número válido"})
			return
		}
		var dadosAtualizados Livro
		if err := c.ShouldBindJSON(&dadosAtualizados); err != nil {
			c.JSON(400, gin.H{"error": "dados inválidos"})
			return
		}
		err = servicoAtualizarLivro(uint(idUint), dadosAtualizados)
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao procurar livro por id para edição"})
			return
		}
		c.JSON(200, "livro editado com sucesso")
	})
	r.DELETE("/livros/:id", func(c *gin.Context) {
		idStr := c.Param("id")
		idUint, err := strconv.ParseUint(idStr, 10, 64)
		if err != nil {
			c.JSON(400, gin.H{"error": "o id deve ser um número válido"})
			return
		}
		err = servicoDeletarLivro(uint(idUint))
		if err != nil {
			c.JSON(500, gin.H{"error": "erro ao deletar livro"})
			return
		}
		c.JSON(200, "livro deletado com sucesso")
	})
	r.Run("localhost:8000")
}
