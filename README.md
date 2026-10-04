# Gerenciador de Senhas

Gerenciador de senhas desenvolvido em Python utilizando Flask e SQLite. O projeto permite criar uma conta, realizar login e armazenar senhas de diferentes serviços de forma criptografada.

## Sobre o projeto

O projeto foi desenvolvido como uma aplicação prática para estudar desenvolvimento backend com Python, Flask, bancos de dados relacionais e conceitos de segurança no armazenamento de credenciais.

A aplicação possui autenticação de usuários e permite registrar senhas de serviços como GitHub, Instagram, Discord, entre outros.

As senhas principais dos usuários são armazenadas utilizando hash, enquanto as senhas dos serviços são armazenadas utilizando criptografia simétrica com Fernet.

## Funcionalidades

- Cadastro de usuários
- Login e autenticação
- Controle de acesso por usuário
- Hash da senha principal
- Geração de chave de criptografia
- Cadastro de senhas de serviços
- Criptografia das senhas armazenadas
- Descriptografia das senhas utilizando a chave
- Associação das senhas ao usuário autenticado
- Banco de dados SQLite
- Interface web com HTML e CSS
- Proteção da chave secreta do Flask através de variável de ambiente

## Tecnologias

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Werkzeug
- Cryptography
- Fernet
- python-dotenv

## Estrutura do projeto

```text
sistema-de-login/
│
├── .env
├── .gitignore
│
├── backend/
│   ├── main.py
│   ├── site_flask.py
│   ├── tabela.py
│   └── usuarios.db
│
└── frontend/
    ├── static/
    │   └── style.css
    │
    └── templates/
        ├── index.html
        └── senhas.html
```

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd sistema-de-login
```

Instale as dependências:

```bash
pip install flask werkzeug cryptography python-dotenv
```

## Configuração do ambiente

O projeto utiliza um arquivo `.env` para armazenar informações sensíveis, como a chave secreta utilizada pelo Flask.

Na raiz do projeto, crie um arquivo chamado:

```text
.env
```

Adicione:

```env
FLASK_SECRET_KEY=sua_chave_secreta
```

Para gerar uma chave aleatória segura, execute:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado para o arquivo `.env`.

Exemplo:

```env
FLASK_SECRET_KEY=8f3a9c7e...
```

O arquivo `.env` não deve ser enviado para o GitHub.

O projeto utiliza um `.gitignore` para impedir que informações sensíveis sejam versionadas:

```text
.env
__pycache__/
*.pyc
```

## Executando o projeto

Entre na pasta `backend`:

```bash
cd backend
```

Execute:

```bash
python main.py
```

Depois acesse:

```text
http://127.0.0.1:5000
```

## Como funciona

### Cadastro

Ao criar uma conta, a senha principal do usuário não é armazenada diretamente no banco de dados.

Ela passa por um processo de hashing utilizando o Werkzeug:

```text
Senha
  ↓
Hash
  ↓
Banco de dados
```

A aplicação também gera uma chave Fernet que deve ser guardada pelo usuário.

### Login

Durante o login, a senha fornecida pelo usuário é comparada com o hash armazenado no banco de dados.

Após a autenticação, o ID do usuário é armazenado na sessão:

```text
Login
  ↓
Verificação da senha
  ↓
Sessão autenticada
  ↓
ID do usuário
```

O ID presente na sessão é utilizado para garantir que cada usuário tenha acesso somente às suas próprias senhas.

### Armazenamento das senhas

Para cadastrar uma senha de serviço, o usuário informa:

- Serviço
- Chave de criptografia
- Senha

A senha é criptografada antes de ser armazenada:

```text
Senha original
       ↓
     Fernet
       ↓
Senha criptografada
       ↓
   SQLite
```

O banco de dados não armazena a senha original.

### Descriptografia

Quando o usuário deseja visualizar suas senhas, ele informa sua chave Fernet.

A aplicação utiliza essa chave para descriptografar as senhas armazenadas:

```text
Senha criptografada
       ↓
   Chave Fernet
       ↓
Senha original
```

## Banco de dados

O projeto utiliza SQLite com duas tabelas principais.

### usuarios

Armazena os dados de autenticação:

```text
id
login
senha
```

### senhas

Armazena as credenciais dos serviços:

```text
id
usuario_id
servico
senha
```

A coluna `usuario_id` relaciona cada senha ao usuário que a cadastrou.

As consultas de senhas utilizam o ID do usuário autenticado para impedir que um usuário consulte as credenciais pertencentes a outro.

## Segurança

O projeto utiliza diferentes mecanismos para proteger as credenciais.

### Senha de login

A senha principal não é armazenada diretamente. Ela é transformada em um hash utilizando o Werkzeug.

### Senhas dos serviços

As senhas dos serviços precisam ser recuperadas posteriormente, portanto são criptografadas utilizando Fernet.

### Chave do Flask

A `SECRET_KEY` utilizada pelo Flask não fica diretamente no código-fonte.

Ela é armazenada no `.env` e carregada através do `python-dotenv`.

```text
.env
  ↓
python-dotenv
  ↓
FLASK_SECRET_KEY
  ↓
Flask Session
```

O `.env` está incluído no `.gitignore` para evitar que a chave seja enviada ao repositório.

### Chave Fernet

A chave utilizada para criptografar as senhas dos serviços não é armazenada no banco de dados.

Por isso, caso o usuário perca sua chave Fernet, as senhas criptografadas não poderão ser recuperadas pela aplicação.

## Objetivo

O principal objetivo do projeto é colocar em prática conceitos de:

- Desenvolvimento backend
- Flask
- SQLite
- Autenticação
- Controle de acesso
- Hashing
- Criptografia
- Gerenciamento de sessões
- Variáveis de ambiente
- Relacionamento entre tabelas
- Desenvolvimento de aplicações web
- Organização de projetos Python

## Observação

Este projeto foi desenvolvido com fins educacionais para estudar desenvolvimento web, autenticação e conceitos de segurança.

Para uma aplicação real em produção, seriam necessários mecanismos adicionais de segurança, como gerenciamento profissional de chaves, proteção contra ataques, HTTPS, políticas de sessão, validação de entrada e outras medidas de segurança.