# 01: Escopo e Requisitos — EstoqueFácil

| Item | Descrição |
|---|---|
| **Sistema** | EstoqueFácil: Controle de Estoque para Pequenos Comércios |
| **Versão do documento** | 1.0 |
| **Autor** | [@Carlosvpontes](https://github.com/Carlosvpontes) |
| **Plataforma** | Aplicação Web |

---

## 1. Contexto e problema

Pequenos comércios (mercadinhos, papelarias, lojas de bairro) costumam controlar o estoque
em cadernos ou planilhas soltas. Isso causa:

- **Falta de produtos na prateleira**, porque ninguém percebe que o estoque está acabando;
- **Compras desnecessárias**, porque não se sabe quanto existe de cada item;
- **Ausência de histórico**: não há registro de quem retirou ou repôs mercadoria, nem quando;
- **Erros de contagem** e perda de tempo para conferir o estoque.

## 2. Objetivos

**Objetivo geral:** oferecer um sistema web simples para que o pequeno comerciante saiba,
a qualquer momento, **o que tem, quanto tem e o que precisa repor**.

**Objetivos específicos:**
1. Centralizar o cadastro de produtos, categorias e fornecedores;
2. Registrar todas as entradas e saídas de mercadoria, com data, hora e responsável;
3. Impedir saídas maiores que a quantidade disponível;
4. Alertar automaticamente sobre produtos com estoque baixo;
5. Exibir um painel com a situação geral do estoque.

## 3. Público-alvo e atores

| Ator | Descrição |
|---|---|
| **Usuário** | Dono(a) ou funcionário(a) do comércio. Usa o sistema no computador ou no celular para cadastrar produtos e registrar movimentações. Não precisa ter conhecimento técnico. |

> Nesta versão existe um único perfil de acesso: todo usuário autenticado tem as mesmas permissões.

---

## 4. Requisitos funcionais (o que o sistema faz)

| ID | Requisito | Prioridade | Regras |
|---|---|---|---|
| **RF01** | Cadastrar conta de usuário (nome, e-mail e senha) | Essencial | RN08 |
| **RF02** | Entrar (login) e sair (logout) do sistema | Essencial | RN09 |
| **RF03** | Manter categorias: incluir, listar, editar e excluir | Essencial | RN06 |
| **RF04** | Manter fornecedores: incluir, listar, editar e excluir (nome, CNPJ, telefone, e-mail) | Essencial | RN06 |
| **RF05** | Manter produtos: incluir, listar, editar e excluir (código, nome, descrição, categoria, fornecedor, preço de custo, preço de venda, estoque mínimo) | Essencial | RN03, RN05, RN07 |
| **RF06** | Registrar **entrada** de mercadoria (produto, quantidade, observação) | Essencial | RN02, RN10 |
| **RF07** | Registrar **saída** de mercadoria (produto, quantidade, observação) | Essencial | RN01, RN02, RN10 |
| **RF08** | Consultar histórico de movimentações, com filtro por produto, tipo (entrada/saída) e período | Essencial | RN11 |
| **RF09** | Exibir painel inicial: total de produtos, valor total do estoque, produtos com estoque baixo e últimas movimentações | Essencial | RN04 |
| **RF10** | Pesquisar produtos por nome ou código e filtrar por categoria | Desejável | — |
| **RF11** | Listar todos os produtos com estoque baixo (relatório de reposição) | Desejável | RN04 |

## 5. Regras de negócio (as "leis" do sistema)

| ID | Regra |
|---|---|
| **RN01** | Uma **saída não pode ser maior** que a quantidade atual em estoque. O sistema bloqueia e mostra a quantidade disponível. |
| **RN02** | A quantidade de uma movimentação deve ser um **número inteiro maior que zero**. |
| **RN03** | A quantidade em estoque de um produto **só muda por meio de movimentações**. Ela não pode ser editada diretamente no cadastro do produto. Todo produto novo começa com estoque zero. |
| **RN04** | Um produto está com **estoque baixo** quando a quantidade atual é **menor ou igual** ao estoque mínimo. Esses produtos aparecem em destaque. |
| **RN05** | O **código do produto é único**: não podem existir dois produtos com o mesmo código. |
| **RN06** | Não é permitido excluir uma **categoria** ou um **fornecedor** que tenha produtos vinculados. |
| **RN07** | Não é permitido excluir um **produto que já tenha movimentações**, para preservar o histórico. |
| **RN08** | O **e-mail do usuário é único** e a senha deve ter **no mínimo 6 caracteres**. |
| **RN09** | Somente usuários autenticados acessam as telas do sistema (exceto login e cadastro de conta). |
| **RN10** | Cada movimentação registra **automaticamente** a data, a hora e o usuário responsável. |
| **RN11** | Movimentações **não podem ser editadas nem excluídas**. Um lançamento errado é corrigido com uma movimentação inversa (ex.: uma entrada registrada a mais é corrigida com uma saída). |
| **RN12** | Preços de custo e de venda não podem ser negativos. O estoque mínimo deve ser zero ou maior. |

## 6. Requisitos não funcionais (como o sistema deve ser)

| ID | Categoria | Requisito |
|---|---|---|
| **RNF01** | Usabilidade | Interface em português, com mensagens claras de sucesso, erro e confirmação |
| **RNF02** | Usabilidade | Layout responsivo: funciona no computador e no celular (Bootstrap) |
| **RNF03** | Usabilidade | Toda exclusão pede confirmação antes de ser executada |
| **RNF04** | Segurança | Senhas armazenadas com criptografia (hash), nunca em texto puro |
| **RNF05** | Segurança | Telas internas protegidas por login; sessão encerrada no logout |
| **RNF06** | Desempenho | Páginas devem carregar em até 2 segundos em uso normal |
| **RNF07** | Compatibilidade | Funcionar nos navegadores Chrome, Edge e Firefox atualizados |
| **RNF08** | Arquitetura | Back-end em Python (Flask) no padrão MVC |
| **RNF09** | Dados | Banco de dados MySQL, com integridade referencial (chaves estrangeiras) |
| **RNF10** | Qualidade | Testes automatizados com pytest para regras de negócio, controllers e telas |
| **RNF11** | Disponibilidade | Publicado na internet (PythonAnywhere) e acessível por um link |
| **RNF12** | Manutenibilidade | Código-fonte aberto e versionado no GitHub |

---

## 7. Fora do escopo (o que o sistema NÃO faz nesta versão)

Para manter o projeto viável no prazo, **não** fazem parte desta versão:

- Vendas / caixa (PDV) e emissão de nota fiscal;
- Controle financeiro (contas a pagar e a receber);
- Pedidos de compra enviados a fornecedores;
- Vários estabelecimentos ou filiais;
- Perfis de permissão diferentes (ex.: administrador × operador);
- Recuperação de senha por e-mail;
- Aplicativo mobile nativo (a versão web já funciona no celular).

---

## 8. Glossário

| Termo | Significado no sistema |
|---|---|
| **Movimentação** | Qualquer registro de entrada ou saída de mercadoria |
| **Entrada** | Mercadoria que chegou (compra, devolução de cliente, ajuste para mais) |
| **Saída** | Mercadoria que saiu (venda, perda, uso interno, ajuste para menos) |
| **Estoque atual** | Soma das entradas menos a soma das saídas de um produto |
| **Estoque mínimo** | Quantidade definida pelo usuário abaixo da qual o produto precisa ser reposto |
| **Valor do estoque** | Soma de (estoque atual × preço de custo) de todos os produtos |

---

## 9. Histórico de revisões

| Versão | Data | Descrição |
|---|---|---|
| 1.0 | 26/10/2026 | Elaboração do escopo: problema, objetivos, requisitos funcionais e não funcionais, regras de negócio e limites do escopo |
