# 02: Avaliações dos Testadores — EstoqueFácil

Cinco pessoas testaram o sistema publicado em https://estoquefacil-f1t6.onrender.com e responderam a um formulário on-line
(Google Forms). As respostas abaixo estão como foram escritas pelos testadores.

> **Privacidade:** como este repositório é público, os testadores aparecem com o primeiro nome e a inicial do sobrenome.
> Os nomes completos constam no formulário de entrega enviado ao tutor.

## Avaliação 1: Eduarda A.

| Campo | Resposta |
|---|---|
| Data do teste | 06/11/2026 |
| O que testou e funcionou | Todas as opções funcionaram perfeitamente |
| O que testou e não funcionou / o que corrigir | O sistema aceita um preço de venda menor do que seu custo, sem me avisar nada. Poderia criar uma opção para que isso não aconteça, pois pode dar prejuízo no cadastro. |
| Funcionalidade não testada | Nada |
| Sugestões de melhoria | Somente a questão do preço de venda ser acima do preço de custo. |

## Avaliação 2: Regiane F.

| Campo | Resposta |
|---|---|
| Data do teste | 06/11/2026 |
| O que testou e funcionou | Todos os testes foram bem positivos, executei entrada e saída em produtos, testei cadastros dos fornecedores, fiz conferência em movimentações. |
| O que testou e não funcionou / o que corrigir | A tela do estoque baixo, ela não sugere a quantidade de produtos, que eu preciso comprar, ela demostra que meu estoque está baixo, poderia aderir ao sistema uma coluna de quantidade sugerida para reposição. |
| Funcionalidade não testada | Nada |
| Sugestões de melhoria | Somente a questão da quantidade sugerida para reposição de produto. |

## Avaliação 3: César R.

| Campo | Resposta |
|---|---|
| Data do teste | 06/11/2026 |
| O que testou e funcionou | Testei todos os parâmetros e funcionou tranquilamente, produtos, cadastro, tanto a entrada, quanto saída, deram tudo certo. |
| O que testou e não funcionou / o que corrigir | Tudo funcionou certinho |
| Funcionalidade não testada | Nada |
| Sugestões de melhoria | Nada |

## Avaliação 4: Robson P.

| Campo | Resposta |
|---|---|
| Data do teste | 06/11/2026 |
| O que testou e funcionou | As funções de cadastro de fornecedor, estoque dos produtos, quantidades tudo ok |
| O que testou e não funcionou / o que corrigir | Os testes que fiz funcionaram perfeitamente |
| Funcionalidade não testada | Nada |
| Sugestões de melhoria | Nada |

## Avaliação 5: Dyonathan G.

| Campo | Resposta |
|---|---|
| Data do teste | 08/11/2026 |
| O que testou e funcionou | Fiz alguns testes e todos eles funcionaram certinho, na questão abaixo está aquilo que encontrei de diferente. |
| O que testou e não funcionou / o que corrigir | Na aba de procura dos produtos resolver sobre o "acento" ao procurar por exemplo a palavra (café) buscar o produto sem se preocupar como ele está escrito corretamente … exemplo escrever (cafe) sem o "é" e já encontrar o produto. |
| Funcionalidade não testada | Nada! |
| Sugestões de melhoria | Nada! |

## Consolidação

| Indicador | Resultado |
|---|---|
| Testadores | 5 |
| Relataram que as funções testadas funcionaram | 5 |
| Relataram funcionalidade não testada | 0 |
| Sugeriram melhorias | 3 |
| Não relataram problemas nem sugestões | 2 |

| # | Melhoria solicitada | Solicitada por | Decisão |
|---|---|---|---|
| 1 | Avisar ou impedir preço de venda menor que o custo | Eduarda A. | Implementada (D04) |
| 2 | Quantidade sugerida para reposição na tela de estoque baixo | Regiane F. | Implementada (D05) |
| 3 | Pesquisa de produtos sem depender de acentos | Dyonathan G. | Implementada (D06) |

Os detalhes das correções estão no [Laudo de Qualidade](03-laudo-de-qualidade.md).
