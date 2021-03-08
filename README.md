# Match Job Developer - API desenvolvida para fornecer dados de candidatos a partir do Json fornecido dentro do db.py

O objetivo deste projeto é desenvolver uma API que retorne dados de candidados, cidades e
tecnologias.

## Como configurar a aplicação

Faça o clone via github do branch main, crie uma imagem de docker e utilize o comando make run-db para configurar o banco de dados e logo em seguida, make run-app para ativar a Api de forma local. Por fim, utilize respectivamente os comandos make recreate_db e make populate_db para criar o banco de dados local e popular a base de dados.

Caso queira fazer um deploy da aplicação, pode-se utilizar os comandos heroku_ no makefile, 
que servem para fazer o deploy.

## Visualização

A Api foi disponibilizado online via Heroku e pode ser visualizado em:

https://lit-citadel-12163.herokuapp.com/

## Melhorias
- Implementar testes.
- Implementar um Crud Básico


Todo feedback é bem-vindo. 