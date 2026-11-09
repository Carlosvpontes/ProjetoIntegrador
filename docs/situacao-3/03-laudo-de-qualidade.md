# 03: Laudo de Qualidade — EstoqueFácil

## 1. Identificação

| Item | Descrição |
|---|---|
| Sistema | EstoqueFácil: Controle de Estoque para Pequenos Comércios |
| Endereço | https://estoquefacil-f1t6.onrender.com |
| Responsável | Carlos Vinicius Oliveira de Pontes |
| Data do laudo | 09/11/2026 |

## 2. Verificação

O sistema foi construído conforme a especificação?

- **Testes automatizados (pytest):** 169 casos, cobrindo as regras de negócio (RN01 a RN13), os controllers, as telas e a
  configuração. Resultado: **169 aprovados e nenhuma falha**, em SQLite e em PostgreSQL.
  Evidência: [evidencia-testes.txt](../situacao-2/evidencia-testes.txt).
- **Casos de teste por requisito:** 21 casos, todos aprovados, descritos no [plano de testes](01-plano-de-testes.md).
- **Ambiente publicado (Render + Neon):** conferido em 27/10/2026 e novamente em 09/11/2026, após as correções.

## 3. Validação

O sistema atende ao que o usuário precisa?

Cinco pessoas testaram o sistema publicado entre 06/11/2026 e 08/11/2026
([avaliações](02-avaliacoes-testadores.md)).

- **O que funcionou:** os cinco relataram que as funções testadas funcionaram, citando cadastros de produtos e fornecedores,
  entradas e saídas e a conferência das movimentações. Nenhum relatou erro que impedisse o uso.
- **O que foi sugerido:** três melhorias, todas implementadas (D04, D05 e D06).

## 4. Defeitos encontrados e correções

| ID | Defeito | Como foi encontrado | Correção aplicada | Situação |
|---|---|---|---|---|
| D01 | Um produto recém-criado, ainda não salvo, recusava a primeira entrada de mercadoria (erro interno) | Carga dos dados de exemplo durante o desenvolvimento (26/10/2026) | O produto passa a nascer com estoque zero; criado teste automatizado | Corrigido |
| D02 | Falha de conexão com o banco exibia mensagem técnica extensa e ilegível | Simulação de publicação com banco inexistente (27/10/2026) | Mensagem curta orientando a conferir a configuração, com a senha oculta | Corrigido |
| D03 | O login podia falhar com "Sua sessão expirou" em navegadores que ocultam a página de origem (Referer) | Teste no ambiente publicado (27/10/2026) | Proteção CSRF mantida pelo token obrigatório; exigência do Referer removida; cookie com SameSite=Lax; testes criados | Corrigido |
| D04 | O sistema aceitava preço de venda menor que o preço de custo, sem avisar | Teste de usuário: Eduarda A. (06/11/2026) | O cadastro exibe um aviso e só aceita o valor após confirmação (RN13); testes criados | Corrigido |
| D05 | A tela de estoque baixo não sugeria a quantidade a comprar | Teste de usuário: Regiane F. (06/11/2026) | Coluna "Sugestão de compra" no painel e no filtro de estoque baixo (dobro do mínimo menos o estoque atual); testes criados | Corrigido |
| D06 | A pesquisa não encontrava produtos com acento quando digitados sem acento (ex.: "cafe" e "Café") | Teste de usuário: Dyonathan G. (08/11/2026) | A pesquisa passa a ignorar acentos e maiúsculas; testes criados | Corrigido |

## 5. Evidências

| Evidência | Local |
|---|---|
| Saída completa dos testes automatizados | [evidencia-testes.txt](../situacao-2/evidencia-testes.txt) |
| Aviso de preço de venda menor que o custo (D04) | [print](../situacao-2/prints/05-produto-aviso-preco.png) |
| Coluna "Sugestão de compra" (D05) | [print](../situacao-2/prints/06-estoque-baixo.png) |
| Demonstração das correções em vídeo | https://youtu.be/NXJucaJNh7Y |

## 6. Limitações conhecidas

As limitações estão listadas na [seção 6 do plano de testes](01-plano-de-testes.md#6-limitações-conhecidas). As principais:
os cinco usuários não repetiram os testes depois das correções, e desempenho e compatibilidade entre navegadores não tiveram
medição formal.

## 7. Conclusão

A verificação e a validação indicam que as funcionalidades principais do EstoqueFácil operam conforme a especificação. As
três melhorias apontadas pelos usuários foram implementadas, cobertas por testes automatizados e publicadas em 09/11/2026.
O sistema atende ao objetivo proposto, dentro do escopo definido.
