# Sistema de Gerenciamento de Veículos

Bem-vindo ao **Sistema de Gerenciamento de Veículos**, uma aplicação web desenvolvida para facilitar o cadastro, edição, listagem e exclusão de veículos. Este projeto utiliza **Flask** como framework backend, **SQLite** como banco de dados e templates HTML com Jinja2 para a interface do usuário. Abaixo, você encontrará uma documentação detalhada e didática para entender, instalar e executar o sistema.

---

## 📋 Visão Geral

O sistema permite gerenciar informações de veículos, como modelo, marca, ano e placa, de forma simples e intuitiva. Ele é ideal para quem deseja aprender sobre desenvolvimento web com Python, Flask e SQLite, ou precisa de uma aplicação leve para gerenciamento de dados.

### Funcionalidades
- **Listar veículos**: Exibe todos os veículos cadastrados em uma tabela com opções de edição e exclusão.
- **Cadastrar veículo**: Permite adicionar um novo veículo ao banco de dados.
- **Editar veículo**: Atualiza as informações de um veículo existente.
- **Excluir veículo**: Remove um veículo após confirmação.
- **Tratamento de erros**: Inclui uma página personalizada para erros 404 (página não encontrada).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação do backend.
- **Flask**: Framework web leve para Python.
- **SQLite**: Banco de dados leve e embutido.
- **HTML/CSS**: Para a interface do usuário.
- **Jinja2**: Motor de templates para renderização dinâmica no Flask.
- **Cloudflare (scripts)**: Scripts de proteção contra bots incluídos nos templates HTML.

---

## 📂 Estrutura do Projeto

Abaixo está a organização dos arquivos do projeto:

```
├── app.py                   # Arquivo principal com a lógica do Flask
├── database/
│   └── db-veiculos.db       # Banco de dados SQLite (gerado automaticamente)
├── templates/
│   ├── 404.html             # Página de erro 404
│   ├── cadastrar.html       # Formulário para cadastro de veículos
│   ├── editar.html          # Formulário para edição de veículos
│   ├── excluir.html         # Página de confirmação de exclusão
│   ├── index.html           # Página inicial com menu de navegação
│   └── listar.html          # Página com a lista de veículos
└── README.md                # Este arquivo
```

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o sistema localmente.

### Pré-requisitos
- **Python 3.x** instalado (recomendado: Python 3.8 ou superior).
- **pip** (gerenciador de pacotes do Python).
- Um terminal ou IDE (como VSCode, PyCharm, etc.).

### Passo a Passo

1. **Clone o repositório ou crie os arquivos**
   - Se você recebeu os arquivos, coloque-os em uma pasta no seu computador.
   - Caso esteja em um repositório Git, clone com:
     ```bash
     git clone <URL_DO_REPOSITORIO>
     cd <NOME_DA_PASTA>
     ```

2. **Crie um ambiente virtual**
   - Isso isola as dependências do projeto. No terminal, execute:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - No Windows:
       ```bash
       venv\Scripts\activate
       ```
     - No Linux/Mac:
       ```bash
       source venv/bin/activate
       ```

3. **Instale as dependências**
   - Com o ambiente virtual ativado, instale o Flask:
     ```bash
     pip install flask
     ```

4. **Crie o banco de dados**
   - O banco de dados SQLite será criado automaticamente ao executar o projeto, mas você precisa criar a tabela `veiculos`. Execute o seguinte código Python em um arquivo temporário (ou no terminal Python):
     ```python
     import sqlite3

     conn = sqlite3.connect('database/db-veiculos.db')
     cursor = conn.cursor()
     cursor.execute('''
         CREATE TABLE IF NOT EXISTS veiculos (
             idveiculo INTEGER PRIMARY KEY AUTOINCREMENT,
             modelo TEXT NOT NULL,
             marca TEXT NOT NULL,
             ano INTEGER NOT NULL,
             placa TEXT NOT NULL,
             datacriacao TEXT NOT NULL
         )
     ''')
     conn.commit()
     conn.close()
     ```
   - Isso criará o arquivo `db-veiculos.db` na pasta `database/`.

5. **Execute a aplicação**
   - No terminal, com o ambiente virtual ativado, execute:
     ```bash
     python app.py
     ```
   - A aplicação será iniciada em `http://127.0.0.1:5000` (localhost).

6. **Acesse o sistema**
   - Abra um navegador e visite: `http://127.0.0.1:5000`
   - Você verá a página inicial com opções para listar ou cadastrar veículos.

---

## 🌐 Como Usar o Sistema

### 1. Página Inicial (`/`)
- Exibe um menu com links para:
  - **Listar Veículos**: Mostra todos os veículos cadastrados.
  - **Cadastrar Veículo**: Abre o formulário de cadastro.

### 2. Listar Veículos (`/veiculos/listar`)
- Exibe uma tabela com os veículos cadastrados, incluindo:
  - ID, Modelo, Marca, Ano, Placa.
  - Ações: Links para **Editar** ou **Deletar** cada veículo.

### 3. Cadastrar Veículo (`/veiculos/cadastrar`)
- Preencha o formulário com:
  - **Modelo**: Nome do veículo (ex.: Civic).
  - **Marca**: Fabricante (ex.: Honda).
  - **Ano**: Ano de fabricação (ex.: 2020).
  - **Placa**: Placa do veículo (ex.: ABC-1234).
- Após enviar, uma mensagem de sucesso será exibida.

### 4. Editar Veículo (`/veiculos/editar/<id>`)
- Abre um formulário preenchido com os dados do veículo selecionado.
- Atualize os campos desejados e clique em **Atualizar**.
- Você será redirecionado para a lista de veículos.

### 5. Excluir Veículo (`/veiculos/deletar/<id>`)
- Exibe uma página de confirmação com o modelo do veículo.
- Clique em **Excluir** para remover o veículo.
- Você será redirecionado para a lista de veículos.

### 6. Página 404
- Se acessar uma rota inexistente, uma página personalizada de erro 404 será exibida.

---

## 🛠️ Detalhes Técnicos

### Banco de Dados
- **Tabela `veiculos`**:
  - `idveiculo`: Chave primária, auto-incrementada.
  - `modelo`: Texto, obrigatório.
  - `marca`: Texto, obrigatório.
  - `ano`: Inteiro, obrigatório.
  - `placa`: Texto, obrigatório.
  - `datacriacao`: Texto (data no formato ISO, ex.: `2025-04-28`).

### Rotas do Flask
| Rota                        | Método | Descrição                              |
|-----------------------------|--------|----------------------------------------|
| `/`                         | GET    | Exibe a página inicial.                |
| `/veiculos/listar`          | GET    | Lista todos os veículos.               |
| `/veiculos/cadastrar`       | GET, POST | Exibe e processa o formulário de cadastro. |
| `/veiculos/editar/<id>`     | GET, POST | Exibe e processa o formulário de edição.   |
| `/veiculos/deletar/<id>`    | GET, POST | Exibe e processa a exclusão de um veículo. |
| Erro 404                    | -      | Exibe a página de erro personalizada.  |

### Segurança
- Os templates HTML incluem scripts da Cloudflare para proteção contra bots.
- Validações básicas são feitas no backend (ex.: verificação de campos obrigatórios e tipo de dado para o ano).

---

## 🎨 Estilização

- A página `404.html` possui CSS embutido para uma aparência amigável e centralizada.
- As demais páginas (`cadastrar.html`, `editar.html`, `excluir.html`, `index.html`, `listar.html`) não possuem CSS aplicado, mas podem ser estilizadas adicionando uma seção `<style>` ou um arquivo CSS externo.
- Sugestão: Adicione um arquivo `static/style.css` e referencie-o nos templates com `{{ url_for('static', filename='style.css') }}`.

---

## 🔧 Possíveis Melhorias

1. **Estilização**: Adicionar CSS consistente para todas as páginas, usando um framework como Bootstrap ou Tailwind CSS.
2. **Validações**: Implementar validações mais robustas (ex.: formato da placa, ano válido).
3. **Autenticação**: Adicionar login para restringir o acesso ao sistema.
4. **Filtros e Busca**: Incluir opções de busca e filtragem na lista de veículos.
5. **Mensagens de Feedback**: Exibir mensagens de sucesso/erro em todas as operações.
6. **Testes**: Criar testes unitários para as rotas e funções do Flask.

---

## ❓ Solução de Problemas

- **Erro: "No module named flask"**
  - Certifique-se de que o Flask está instalado (`pip install flask`) no ambiente virtual ativo.
- **Erro: Banco de dados não encontrado**
  - Verifique se a pasta `database/` existe e se o arquivo `db-veiculos.db` foi criado.
  - Execute o script de criação da tabela fornecido acima.
- **Página em branco ou erro 500**
  - Verifique o terminal para erros detalhados (o modo debug está ativado em `app.run(debug=True)`).
- **Links não funcionam**
  - Confirme que as rotas nos templates correspondem às definidas em `app.py`.
