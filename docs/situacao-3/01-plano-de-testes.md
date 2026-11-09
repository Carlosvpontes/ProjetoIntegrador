# 01: Plano e Resultado dos Testes — EstoqueFácil

| Item | Descrição |
|---|---|
| Objetivo | Demonstrar que o sistema foi construído conforme a especificação (**verificação**) e atende às necessidades dos usuários (**validação**) |
| Base | [Requisitos e regras de negócio](../situacao-1/01-escopo-e-requisitos.md) |
| Última execução | 09/11/2026 |

## 1. Níveis de teste

| Nível (Modelo V) | Tipo | Como foi feito |
|---|---|---|
| Teste unitário | Verificação | pytest, sobre as regras de negócio da camada Model e as funções de apoio |
| Teste de integração | Verificação | pytest com o cliente de testes do Flask, passando por rotas, controllers, banco de dados e telas |
| Teste de sistema | Verificação | Conferência no ambiente publicado (Render + Neon) |
| Teste de aceitação | Validação | Cinco usuários testaram o sistema publicado e responderam a um formulário |

## 2. Verificação: testes automatizados

Saída completa da execução: [evidencia-testes.txt](../situacao-2/evidencia-testes.txt).

| Arquivo | O que cobre | Testes |
|---|---|---|
| `test_auth.py` | Criar conta, login, logout e proteção das páginas | 14 |
| `test_categorias.py` | Cadastro de categorias | 11 |
| `test_configuracao.py` | Conexão com o banco, variáveis de ambiente e proteção CSRF | 12 |
| `test_formularios.py` | Leitura de preços, números e pesquisa sem acentos | 31 |
| `test_fornecedores.py` | Cadastro de fornecedores | 9 |
| `test_models.py` | Regras de negócio e restrições do banco | 37 |
| `test_movimentacoes.py` | Entradas, saídas e histórico | 21 |
| `test_painel.py` | Painel e página de erro | 6 |
| `test_produtos.py` | Cadastro, pesquisa e filtros de produtos | 28 |
| **Total** | | **169** |

**Resultado:** 169 aprovados e nenhuma falha, em SQLite (ambiente local) e em PostgreSQL (mesmo SGBD da produção).

## 3. Verificação: casos de teste por requisito

Cada caso está ligado aos testes automatizados que o comprovam, permitindo rastrear requisito, código e teste.

| ID | Requisito | Cenário | Resultado esperado | Testes automatizados | Situação |
|---|---|---|---|---|---|
| CT01 | RF01, RN08 | Criar conta com dados válidos e com e-mail repetido | Conta criada; e-mail repetido recusado | `test_cadastro_com_sucesso`, `test_cadastro_com_email_repetido` | Aprovado |
| CT02 | RF02 | Entrar com senha certa e errada; sair | Acesso liberado; senha errada recusada; sessão encerrada | `test_login_com_sucesso_vai_para_o_painel`, `test_login_com_senha_errada`, `test_logout` | Aprovado |
| CT03 | RN09 | Abrir página interna sem login | Redireciona ao login | `test_pagina_interna_exige_login` | Aprovado |
| CT04 | RF03 | Incluir, editar e excluir categoria | Operações concluídas | `test_incluir_categoria`, `test_editar_categoria`, `test_excluir_categoria_sem_produtos` | Aprovado |
| CT05 | RN06 | Excluir categoria com produtos | Exclusão bloqueada | `test_nao_exclui_categoria_com_produtos` | Aprovado |
| CT06 | RF04, RN06 | Incluir fornecedor, CNPJ incompleto e excluir com produtos | CNPJ validado; exclusão bloqueada | `test_incluir_fornecedor_guarda_cnpj_somente_com_digitos`, `test_cnpj_incompleto`, `test_nao_exclui_fornecedor_com_produtos` | Aprovado |
| CT07 | RF05 | Incluir, editar e excluir produto | Operações concluídas | `test_incluir_produto`, `test_editar_produto`, `test_excluir_produto_sem_movimentacoes` | Aprovado |
| CT08 | RN03 | Enviar quantidade pelo cadastro do produto | Estoque não muda | `test_formulario_nao_altera_quantidade_em_estoque` | Aprovado |
| CT09 | RN05 | Cadastrar código repetido | Cadastro recusado | `test_codigo_repetido` | Aprovado |
| CT10 | RN07 | Excluir produto com movimentações | Exclusão bloqueada | `test_nao_exclui_produto_com_movimentacoes` | Aprovado |
| CT11 | RN13 | Venda menor que o custo, sem e com confirmação | Pede confirmação; salva após confirmar | `test_venda_menor_que_custo_pede_confirmacao`, `test_venda_menor_que_custo_com_confirmacao_e_salva` | Aprovado |
| CT12 | RF06, RN10 | Registrar entrada | Estoque aumenta; usuário registrado | `test_registrar_entrada` | Aprovado |
| CT13 | RF07 | Registrar saída | Estoque diminui | `test_registrar_saida` | Aprovado |
| CT14 | RN01 | Saída maior que o estoque | Saída bloqueada; estoque mantido | `test_saida_maior_que_estoque_e_bloqueada` | Aprovado |
| CT15 | RN02 | Quantidade zero, negativa ou não inteira | Operação recusada | `test_quantidade_invalida` | Aprovado |
| CT16 | RF08 | Filtrar histórico por produto, tipo e período | Lista somente o filtrado | `test_historico_filtra_por_produto`, `test_historico_filtra_por_tipo`, `test_historico_filtra_por_periodo_incluindo_o_ultimo_dia` | Aprovado |
| CT17 | RN11 | Tentar editar ou excluir movimentação | Operação inexistente | `test_movimentacoes_nao_podem_ser_editadas_nem_excluidas` | Aprovado |
| CT18 | RF09, RN04 | Abrir painel com estoque baixo | Totais e alerta corretos | `test_painel_mostra_totais_e_estoque_baixo` | Aprovado |
| CT19 | RF10 | Pesquisar sem acento e por código | Produto encontrado | `test_pesquisa_ignora_acentos_nos_dois_sentidos`, `test_pesquisa_por_codigo` | Aprovado |
| CT20 | RF11 | Filtrar estoque baixo | Mostra a sugestão de compra | `test_filtro_estoque_baixo_mostra_quantidade_sugerida` | Aprovado |
| CT21 | RNF01 | Abrir endereço inexistente | Página de erro amigável | `test_pagina_inexistente_mostra_erro_404` | Aprovado |

## 4. Verificação: ambiente publicado

| Data | O que foi conferido | Resultado |
|---|---|---|
| 27/10/2026 | Login, painel, cadastros e histórico acessíveis; acentuação correta; página 404; cookie de sessão protegido por HTTPS | Aprovado |
| 09/11/2026 | Login, coluna "Sugestão de compra" no painel e no filtro de estoque baixo, pesquisa `cafe` encontrando "Café" | Aprovado |

## 5. Validação: testes com usuários

Cinco pessoas testaram o sistema publicado entre 06/11/2026 e 08/11/2026. As respostas estão em
[02-avaliacoes-testadores.md](02-avaliacoes-testadores.md).

## 6. Limitações conhecidas

| Item | Situação |
|---|---|
| RN13 no ambiente publicado | Comprovada pelos testes automatizados; não foi repetida no site publicado para não gravar dados de teste |
| RNF06 (carregamento em até 2 segundos) | Sem medição formal. O primeiro acesso após 15 minutos parado leva cerca de 1 minuto, por limitação do plano gratuito |
| RNF07 (Chrome, Edge e Firefox) | Sem teste formal em cada navegador |
| Saídas simultâneas do mesmo produto | O bloqueio de linha do banco não foi exercitado por um teste de concorrência |
| Reteste pelos usuários | As melhorias foram verificadas por testes automatizados; os cinco usuários não repetiram os testes depois das correções |
