# Web Scraping Livros da Amazon
O objetivo desse projeto foi realizar web scrapping da página com os [100 livros mais vendidos pela Amazon](https://www.amazon.com.br/gp/bestsellers/books/?ie=UTF8&ref_=sv_b_2) coletando informações como nome do livro e autor, preço e avaliações. O resultado final foi gravado em um arquivo estruturado no formato csv

# Observações
- Existem duas páginas com 50 livros cada.
- Não há padrão entre as URLs dessas páginas.
- Cada página faz uso de JavaScript dinâmico, ou seja o carregamento dos livros é gradual com a rolagem da barra lateral do navegador.

# Tecnologias Utilizadas
- Python
- BeatifulSoup
- Selenium
- Pandas

# Perspectivas
- Agendar task para o crawler realizar a varredura periodicamente enviando um relatório por e-mail.
