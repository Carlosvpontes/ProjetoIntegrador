# Publicação: Render (site) + Neon (banco de dados)

Guia para colocar o EstoqueFácil na internet **sem custo**.

| Peça | Serviço | Plano | Função |
|---|---|---|---|
| Banco de dados | [Neon](https://neon.tech) | Free | PostgreSQL na nuvem |
| Site | [Render](https://render.com) | Free | Roda o sistema (Python/Flask) e gera o link público |
| Código | [GitHub](https://github.com/Carlosvpontes/ProjetoIntegrador) | — | O Render baixa o código daqui |

```mermaid
flowchart LR
    U[Usuário<br/>navegador] -->|HTTPS| R[Render<br/>site EstoqueFácil]
    R -->|SQL| N[(Neon<br/>PostgreSQL)]
    G[GitHub<br/>código-fonte] -->|publica automaticamente| R
```

**Tempo estimado:** 20 a 30 minutos. **Não é preciso instalar nada nem digitar comandos.**

> 🔒 **Atenção:** a *connection string* do Neon (parte A) **contém a senha do banco**.
> Cole-a **somente** no Render (parte B). Não envie por chat, e-mail ou WhatsApp e não salve no GitHub.

> ℹ️ Os sites mudam o visual com o tempo. Se um botão tiver um nome um pouco diferente do
> descrito aqui, procure a opção equivalente.

---

## Parte A: criar o banco de dados no Neon

1. Acesse **https://neon.tech** e clique em **Sign up**.
2. Escolha **Continue with GitHub** e autorize com a conta **Carlosvpontes** (assim não precisa criar outra senha).
3. Na tela de criação do projeto, preencha:

   | Campo | Valor |
   |---|---|
   | Project name | `estoquefacil` |
   | Postgres version | deixe a versão sugerida |
   | Cloud provider | **AWS** |
   | Region | **AWS US East 1 (N. Virginia)** |

   Clique em **Create project**.
   > A região precisa ser a **mesma do site** (o Render usa "Virginia", nos EUA). Assim o sistema fica mais rápido.

4. No painel do projeto, clique no botão **Connect** (canto superior direito).
5. Na janela **Connect to your database**:
   - **Branch:** `main` · **Database:** `neondb` · **Role:** `neondb_owner` (os valores que já vêm marcados);
   - **Desligue** a opção **Connection pooling** (se estiver ligada);
   - No seletor de formato, escolha **Connection string**;
   - Clique em **Show password** para a senha aparecer no texto (sem isso, ela vem como `****`);
   - Clique em **Copy snippet** (ícone de copiar).
6. O texto copiado tem este formato:
   ```
   postgresql://neondb_owner:SENHA@ep-xxxx-xxxx.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```
   Deixe-o copiado (ou cole temporariamente no Bloco de Notas, **sem salvar o arquivo**).

✅ **Pronto quando:** você tem a connection string começando com `postgresql://` e **sem** `****` no lugar da senha.

> As tabelas **não** precisam ser criadas à mão: o Render faz isso sozinho na parte B.

---

## Parte B: publicar o site no Render

1. Acesse **https://render.com** e clique em **Get Started** (ou **Sign up**).
2. Escolha **GitHub** e autorize com a conta **Carlosvpontes**.
3. No painel (Dashboard), clique em **New +** → **Blueprint**.
   > "Blueprint" significa que o Render vai ler o arquivo [`render.yaml`](../../render.yaml) do projeto,
   > que já tem toda a configuração pronta.
4. Em **Connect a repository**:
   - Se `Carlosvpontes/ProjetoIntegrador` aparecer na lista, clique em **Connect** ao lado dele;
   - Se **não** aparecer: clique em **Configure account** (ou **Connect GitHub**), escolha
     **Only select repositories**, selecione **ProjetoIntegrador**, clique em **Save/Install** e volte ao Render.
5. Na tela do Blueprint:

   | Campo | Valor |
   |---|---|
   | Blueprint Name | `estoquefacil` |
   | Branch | `main` |

   Mais abaixo aparece o serviço **estoquefacil** (Web Service, plano **Free**) e um campo para a
   variável **`DATABASE_URL`**. **Cole ali a connection string do Neon** (parte A.6).
6. Clique em **Deploy Blueprint** (ou **Apply**).
7. Acompanhe a publicação: clique no serviço **estoquefacil** → aba **Logs** (ou **Events**). Leva de **3 a 6 minutos**.
   No meio do texto devem aparecer estas linhas:
   ```
   Tabelas prontas em: postgresql+psycopg://neondb_owner:***@ep-....neon.tech/neondb
   Dados de exemplo inseridos. Login: demo@estoquefacil.com / senha: demo123
   ...
   Your service is live 🎉
   ```

✅ **Pronto quando:** aparece **"Your service is live"** e o status do serviço fica **Live** (verde).

---

## Parte C: conferir o site

1. No topo da página do serviço **estoquefacil** há o endereço público, por exemplo:
   **`https://estoquefacil.onrender.com`**
   > Se esse nome já estiver em uso por outra pessoa, o Render acrescenta letras no final
   > (ex.: `https://estoquefacil-ab12.onrender.com`). **Anote o endereço exato.** Ele vai para o formulário de entrega.
2. Abra o endereço em uma **aba anônima** do navegador.
3. Entre com `demo@estoquefacil.com` / senha `demo123`.
4. ✅ O painel deve mostrar **10 produtos** e **3 com estoque baixo**, com acentos corretos ("Café Torrado 500g").
5. Faça um teste rápido: **Nova entrada** de 20 unidades de Café Torrado. O estoque deve ir para 22.

📄 **Vai para o formulário de entrega (`PIT_atividade.docx`):**

| Campo | Valor |
|---|---|
| Banco de Dados | PostgreSQL (Neon) |
| Hospedagem | Render |
| Link da solução em funcionamento | o endereço anotado no item C.1 |

---

## Como funciona o plano gratuito (importante para os testadores e para o vídeo)

| Situação | O que acontece | O que fazer |
|---|---|---|
| Site sem acesso por **15 minutos** | O Render "adormece" o site | Nada: ele acorda sozinho no próximo acesso |
| **Primeiro acesso** depois de adormecer | A página demora **cerca de 1 minuto** para abrir | Avise os testadores; **antes de gravar o vídeo**, abra o site e espere carregar |
| Banco sem uso por alguns minutos | O Neon pausa o banco | Nada: ele volta em menos de 1 segundo |

O plano gratuito não tem data de expiração para o site; basta não ultrapassar os limites de uso mensal,
o que este projeto não chega perto de fazer.

---

## Atualizar o site depois de uma correção

**É automático.** Sempre que o código for enviado ao GitHub (pelo Claude), o Render publica a nova
versão sozinho em poucos minutos. Para acompanhar: serviço **estoquefacil** → aba **Events**.

Para forçar uma nova publicação: serviço **estoquefacil** → **Manual Deploy** → **Deploy latest commit**.

---

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Publicação falha com **"Não foi possível conectar ao banco de dados"** | Connection string errada ou incompleta | Serviço **estoquefacil** → **Environment** → edite `DATABASE_URL`, cole de novo a string do Neon → **Save, rebuild, and deploy** |
| Logs mostram **`password authentication failed`** | A string foi copiada com `****` no lugar da senha | Repita A.5 clicando em **Show password** antes de copiar |
| Página **"Application error"** ou **502** | Erro ao iniciar o sistema | Aba **Logs**: copie as últimas 20 linhas e envie ao Claude (a senha aparece como `***`) |
| Site demora ~1 minuto para abrir | O site estava "adormecido" (plano gratuito) | Normal: aguarde |
| Página sem cores/estilo | Bloqueio de internet do navegador | Teste em outra rede ou navegador |
| Repositório não aparece no Render | O Render não tem permissão no GitHub | Parte B.4, opção **Configure account** |
| A connection string vazou (foi enviada a alguém) | Risco de acesso indevido | Neon → **Roles** → `neondb_owner` → **Reset password**; depois atualize `DATABASE_URL` no Render |

---

## Onde ficam as configurações (para referência)

| Arquivo | Para que serve |
|---|---|
| [`render.yaml`](../../render.yaml) | Diz ao Render como instalar (`pip install`), preparar o banco (`criar_banco.py`) e iniciar o site (`gunicorn`) |
| [`config.py`](../../config.py) | Lê `DATABASE_URL` e `SECRET_KEY` e converte a connection string do Neon para o formato usado pelo sistema |
| [`criar_banco.py`](../../criar_banco.py) | Cria as tabelas e os dados de exemplo. Roda a cada publicação; não apaga nem duplica dados |
| `SECRET_KEY` | Chave que protege o login. **Gerada automaticamente pelo Render** (não é preciso criar) |
