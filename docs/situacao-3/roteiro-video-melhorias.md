# Roteiro do Vídeo 2: Solução atualizada (melhorias após os testes)

| Item | Valor |
|---|---|
| Exigência do professor | Vídeo de **até 5 minutos** apresentando as modificações feitas a partir dos testes dos colegas |
| Duração planejada | **3 a 4 minutos e meio** (margem de segurança abaixo dos 5 min) |
| Quando gravar | **Depois** que os 5 colegas testarem e as correções estiverem publicadas no Render |
| Vai para | `PIT_atividade.docx` → seção **Vídeo da Solução atualizada** → "Link para o vídeo" |

> ⚠️ Este roteiro tem **lacunas** (`[…]`) porque as melhorias dependem do que os testadores relatarem.
> Quando as correções estiverem prontas, o Claude completa as lacunas com os itens reais.

---

## Antes de gravar (checklist)

- [ ] As correções já estão no ar (o Render publica sozinho; confira a aba **Events** ou teste no site).
- [ ] Mesmos cuidados do vídeo 1: site "acordado" 1 a 2 minutos antes, janela anônima, zoom 110–125%, notificações desligadas.
- [ ] Tenha à mão os **prints de "antes"** de cada problema (enviados pelos testadores ou tirados por você)
      na pasta `docs/situacao-3/evidencias/`.
- [ ] Abra o PDF ou a planilha com as **5 avaliações** dos colegas.

---

## Roteiro cena a cena

### Cena 1: Abertura (0:00 a 0:20)
| O que fazer na tela | O que falar |
|---|---|
| Painel do sistema | "Olá! Sou Carlos Vinicius Oliveira de Pontes, RGM 40631559. Neste vídeo apresento as melhorias feitas no EstoqueFácil depois dos testes realizados por cinco colegas." |

### Cena 2: Como foram os testes (0:20 a 1:00)
| O que fazer na tela | O que falar |
|---|---|
| Mostre o formulário do Google Forms e depois a planilha/PDF com as respostas | "Os testes foram feitos por [5] pessoas entre [data inicial] e [data final], usando o sistema publicado e este formulário, que registra nome, data, o que funcionou, o que não funcionou e o que não foi testado. No total foram relatados [N] problemas e [N] sugestões." |

### Cenas 3 a 5: Cada melhoria (1:00 a 4:00, cerca de 1 minuto por item)
Repita este bloco para as **2 ou 3 melhorias mais importantes**:

| O que fazer na tela | O que falar |
|---|---|
| Mostre o **print de "antes"** | "A [nome do colega] relatou que [problema]. Era assim: [descrever]." |
| Faça a mesma ação **no sistema atualizado** | "Agora, [o que mudou]. Por exemplo, [demonstrar]." |

| # | Problema relatado (antes) | Testador | Melhoria (depois) | Como demonstrar |
|---|---|---|---|---|
| 1 | […] | […] | […] | […] |
| 2 | […] | […] | […] | […] |
| 3 | […] | […] | […] | […] |

> Se algum colega sugeriu algo que **não** foi feito, mencione rapidamente o motivo (ex.: "ficou fora do escopo
> desta versão"). O professor pede para **não esconder falhas**.

### Cena 6: Qualidade garantida (4:00 a 4:30)
| O que fazer na tela | O que falar |
|---|---|
| Duplo clique em `rodar_testes.bat` (ou mostre o laudo no GitHub: `docs/situacao-3`) | "Cada correção ganhou um teste automatizado. Agora são [N] testes, todos passando. Os detalhes estão no laudo de qualidade, no repositório." |

### Cena 7: Encerramento (4:30 a 4:45)
| O que fazer na tela | O que falar |
|---|---|
| Painel do sistema | "Essas foram as melhorias do EstoqueFácil a partir do feedback dos usuários. Obrigado!" |

---

## Gravar e publicar

Siga as mesmas instruções do vídeo 1 ([roteiro-video-demonstracao.md](../situacao-2/roteiro-video-demonstracao.md),
seções "Gravar com o Clipchamp" e "Publicar no YouTube"), com estas diferenças:

- **Confira a duração:** precisa ter **5 minutos ou menos**.
- **Título no YouTube:** `EstoqueFácil – PIT Engenharia de Software II – Melhorias após os testes`
- Visibilidade: **Não listado**.

✅ **Depois:** envie o link ao Claude ("o link do vídeo 2 é …") para registrar no README e no `PIT_atividade.docx`.
