# Publicação no PythonAnywhere

Guia para publicar o EstoqueFácil em **https://carlosvpontes.pythonanywhere.com** (plano gratuito).

| Item | Valor |
|---|---|
| Usuário | `carlosvpontes` |
| Banco de dados | MySQL: `carlosvpontes$estoque` |
| Pasta do projeto no servidor | `/home/carlosvpontes/ProjetoIntegrador` |
| Ambiente Python | `venv-estoque` |

> 🔒 **Senhas:** a senha do MySQL é digitada **somente** no console do PythonAnywhere (parte B).
> Ela fica gravada no arquivo `.env` do servidor, que não vai para o GitHub. Não envie essa senha por chat ou e-mail.

---

## Parte A: criar o banco MySQL

1. Entre em https://www.pythonanywhere.com e clique em **Databases** no menu do topo.
2. Na seção **MySQL password**, digite uma senha nova nos dois campos e clique em **Set MySQL password**.
   - Use uma senha **diferente** da senha da sua conta.
   - Anote-a em um lugar seguro. Você vai digitá-la uma vez na parte B.
3. Na seção **Create a database**, digite `estoque` e clique em **Create**.
4. Confira: na lista **Your databases** aparece `carlosvpontes$estoque`.

## Parte B: baixar o código e configurar

1. No menu do topo, clique em **Consoles** e depois em **Bash** (seção "Start a new console").
2. Uma tela preta (terminal) se abre. Cole **um comando por vez** e aperte Enter:

   ```bash
   git clone https://github.com/Carlosvpontes/ProjetoIntegrador.git
   ```
   ```bash
   cd ProjetoIntegrador
   ```
   ```bash
   mkvirtualenv --python=python3.13 venv-estoque
   ```
   > O começo da linha passa a mostrar `(venv-estoque)`.
   > Se aparecer erro dizendo que a versão não existe, use `python3.12` no lugar de `python3.13`.

   ```bash
   pip install -r requirements.txt
   ```
   > Leva de 1 a 3 minutos. No fim aparece "Successfully installed ...".

3. Configure a conexão com o banco:
   ```bash
   python configurar_producao.py
   ```
   - "Usuário do PythonAnywhere": apenas aperte **Enter** (já vem `carlosvpontes`).
   - "Senha do MySQL": digite a senha da parte A e aperte **Enter**. **Ela não aparece enquanto você digita, é normal.**
   - ✅ Deve aparecer: `Conexão OK! Arquivo .env criado.`

4. Crie as tabelas com os dados de exemplo:
   ```bash
   python criar_banco.py --exemplo
   ```
   ✅ Deve aparecer: `Dados de exemplo inseridos.`

5. (Opcional, mas recomendado) Rode os testes no servidor:
   ```bash
   python -m pytest -q
   ```
   ✅ Deve terminar com `passed` e nenhum `failed`.

## Parte C: criar o site

1. No menu do topo, clique em **Web** e depois em **Add a new web app**.
2. Avance com **Next**. Escolha **Manual configuration (including virtualenvs)** (não escolha "Flask").
3. Escolha a **mesma versão do Python** usada no passo B.2 (ex.: **Python 3.13**) → **Next**.
4. Na página **Web** que aparece, preencha (clique no texto em vermelho/azul para editar e confirme com ✓):

   | Seção | Campo | Valor |
   |---|---|---|
   | **Code** | Source code | `/home/carlosvpontes/ProjetoIntegrador` |
   | **Code** | Working directory | `/home/carlosvpontes/ProjetoIntegrador` |
   | **Virtualenv** | Enter path to a virtualenv | `/home/carlosvpontes/.virtualenvs/venv-estoque` |

5. Ainda em **Code**, clique no link do **WSGI configuration file**
   (`/var/www/carlosvpontes_pythonanywhere_com_wsgi.py`). Abre um editor:
   - Apague **todo** o conteúdo (Ctrl+A e Delete);
   - Cole o conteúdo do arquivo [`deploy/wsgi_pythonanywhere.py`](../../deploy/wsgi_pythonanywhere.py);
   - Clique em **Save** e volte para a aba **Web**.
6. Na seção **Static files**, clique em "Enter URL" e preencha:

   | URL | Directory |
   |---|---|
   | `/static/` | `/home/carlosvpontes/ProjetoIntegrador/app/static` |

7. Na seção **Security**, ligue **Force HTTPS**.
8. No topo da página, clique no botão verde **Reload carlosvpontes.pythonanywhere.com**.

## Parte D: conferir

1. Abra **https://carlosvpontes.pythonanywhere.com** (de preferência numa aba anônima).
2. Entre com `demo@estoquefacil.com` / senha `demo123`.
3. ✅ O painel deve mostrar 10 produtos e 3 com estoque baixo, com acentos corretos ("Café Torrado 500g").

---

## Atualizar o site depois de uma correção

Sempre que o código mudar no GitHub:

1. **Consoles** → abra o Bash (ou use o que já está aberto) e cole:
   ```bash
   cd ~/ProjetoIntegrador && workon venv-estoque && git pull && pip install -r requirements.txt
   ```
2. **Web** → botão verde **Reload**.

## Manutenção do plano gratuito

- O site fica no ar por **3 meses**. Para renovar: aba **Web** → botão **Run until 3 months from today**.
  Faça isso perto da entrega do trabalho.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| "Something went wrong :-(" ou erro 500 | Aba **Web** → seção **Log files** → abra o **Error log**, copie as últimas linhas e envie ao Claude |
| `mkvirtualenv: command not found` | Feche o console, abra um novo **Bash** e tente de novo |
| Console novo não reconhece o projeto | Rode `cd ~/ProjetoIntegrador && workon venv-estoque` |
| `Access denied for user` no configurar_producao.py | Senha do MySQL errada: redefina na aba **Databases** (parte A.2) e rode o script de novo |
| `Unknown database` | Faltou criar o banco `estoque` (parte A.3) |
| Página sem cores/estilo | Confira o item **Static files** (parte C.6) e clique em **Reload** |
| Mudei o código e o site não mudou | Faltou `git pull` e **Reload** (seção "Atualizar o site") |
