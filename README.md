# northeastern-roots
Projeto de Desenvolvimento Back-end do Curso de Análise e Desenvolvimento de Sistemas
Instruções
O objetivo deste item é mostrar as funcionalidades do sistema, demonstrando suas telas e os procedimentos iniciais para rodar o projeto (as instruções poderão ter pequenas alterações dependendo do sistema operacional utilizado, no caso foi utilizado o Windows 10):
1.	Clonar o repositório no link: https://github.com/marcos-erbas-jr/northeastern-roots ou baixar ele zipado do GitHub
2.	Crie uma nova venv (necessário ter python instalado na máquina): python -m venv venv
3.	Ative a venv: venv\Scripts\activate
4.	Instale as dependências que estão no requirements.txt que está dentro do diretório app/ por meio do comando: pip install -r requirements.txt
5.	Após a instalação das bibliotecas podemos rodar o servidor para testar as funcionalidades do sistema com o comando: uvicorn app.main:app --reload
6.	Será criado um endereço local para acessar o sistema: http://127.0.0.1:8000
   
Obs.: Existe uma seed no projeto para gerar o banco de dados com informações iniciais, mas o projeto já foi para o GitHub com o database.db criado não sendo necessário rodar a seed.py novamente.

Usuários para teste já salvo no banco de dados:
•	email: admin@raizesdonordeste.com  |  senha: 12345678
•	email: atendente@raizesdonordeste.com | senha: 12345678
•	email: cozinha@raizesdonordeste.com | senha: 12345678
