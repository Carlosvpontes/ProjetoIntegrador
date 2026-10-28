# Roteiro do Vídeo 1: Demonstração do EstoqueFácil

| Item | Valor |
|---|---|
| Exigência do professor | Vídeo **narrado**, com **no mínimo 5 minutos**, mostrando a solução em funcionamento |
| Duração planejada | **6 a 7 minutos** (margem de segurança acima dos 5 min) |
| Onde gravar | Sistema publicado: **https://estoquefacil-f1t6.onrender.com** |
| Login usado | `demo@estoquefacil.com` / senha `demo123` |
| Vai para | `PIT_atividade.docx` → tabela **Codificação** → "Link do vídeo narrado" |

---

## Antes de gravar (checklist)

- [ ] **Acorde o site:** abra https://estoquefacil-f1t6.onrender.com **1 a 2 minutos antes** e espere a tela de login aparecer
      (no plano gratuito o primeiro acesso demora ~1 minuto).
- [ ] Use uma **janela anônima** do navegador (Ctrl+Shift+N), para não aparecerem senhas salvas nem favoritos.
- [ ] Deixe abertas, em abas: (1) o sistema; (2) o repositório https://github.com/Carlosvpontes/ProjetoIntegrador.
- [ ] Zoom do navegador em **110% ou 125%** (Ctrl e +), para o texto ficar legível no vídeo.
- [ ] Ative o **Não incomodar** do Windows (Configurações → Sistema → Notificações) e feche WhatsApp e e-mail.
- [ ] Deixe a pasta `ProjetoIntegrador` aberta no Explorador de Arquivos (para a cena 10).
- [ ] Teste o microfone gravando 10 segundos e ouvindo.
- [ ] Leia o roteiro em voz alta uma vez. **Não precisa decorar:** fale com naturalidade usando os tópicos.

---

## Roteiro cena a cena

> **Coluna "O que fazer na tela":** os cliques. **Coluna "O que falar":** sugestão de narração (adapte ao seu jeito).

### Cena 1: Abertura (0:00 a 0:30)
| O que fazer na tela | O que falar |
|---|---|
| Tela de login do sistema | "Olá! Meu nome é Carlos Vinicius Oliveira de Pontes, RGM 40631559. Este é o meu Projeto Integrador Transdisciplinar em Engenharia de Software II: o **EstoqueFácil**, um sistema web de controle de estoque para pequenos comércios." |

### Cena 2: Problema e solução (0:30 a 1:10)
| O que fazer na tela | O que falar |
|---|---|
| Aba do GitHub, mostrando o README (role até "Sobre o projeto") | "Pequenos comércios costumam controlar o estoque em cadernos ou planilhas. Isso gera falta de produtos, compras desnecessárias e nenhum histórico. O EstoqueFácil resolve isso: o comerciante sabe **o que tem, quanto tem e o que precisa repor**." |

### Cena 3: Tecnologias e arquitetura (1:10 a 1:50)
| O que fazer na tela | O que falar |
|---|---|
| No README, role até "Tecnologias" e depois até o diagrama "Arquitetura (MVC)" | "O back-end foi feito em **Python com o framework Flask**, no padrão **MVC**: o *Model* guarda os dados e as regras de negócio, a *View* são as telas em HTML, CSS com Bootstrap e JavaScript, e o *Controller* recebe as ações do usuário. O banco é **PostgreSQL**, hospedado no Neon, e o sistema está publicado no **Render**. Todo o código e a documentação estão neste repositório público no GitHub." |
| Clique na pasta `app` e mostre `models`, `controllers`, `templates` | "Aqui estão as três camadas separadas em pastas." |

### Cena 4: Criar conta e login (1:50 a 2:30)
| O que fazer na tela | O que falar |
|---|---|
| Volte ao sistema → clique em **Criar conta** | "Começando pelo acesso. Na tela de criar conta…" |
| Preencha nome e e-mail, senha `123456` e confirmação `654321` → **Criar conta** | "…se as senhas não conferem, o sistema avisa embaixo do campo e mantém o que foi digitado. As mensagens seguem o catálogo definido na documentação de IHC." |
| Clique em **Entrar** (link no rodapé) → faça login com `demo@estoquefacil.com` / `demo123` | "Vou entrar com o usuário de demonstração. As senhas são guardadas criptografadas no banco." |

### Cena 5: Painel (2:30 a 3:00)
| O que fazer na tela | O que falar |
|---|---|
| Painel aberto; passe o mouse pelos 4 cartões e pela tabela "Precisa repor" | "Este é o painel: total de produtos, valor do estoque, produtos com estoque baixo e movimentações do dia. Em amarelo, o alerta: estes produtos estão com estoque **igual ou abaixo do mínimo** e precisam ser repostos." |

### Cena 6: Categorias e fornecedores (3:00 a 3:40)
| O que fazer na tela | O que falar |
|---|---|
| Menu **Categorias** → **Nova categoria** → nome `Padaria` → **Salvar** | "Os cadastros seguem o mesmo padrão: incluir, listar, editar e excluir. Vou criar a categoria Padaria." |
| Na lista, clique em **Excluir** na categoria **Bebidas** → confirme | "Antes de excluir, o sistema pede confirmação. E aqui uma regra de negócio: não é possível excluir uma categoria que tem produtos vinculados." |
| Menu **Fornecedores** (só mostrar a lista) | "Os fornecedores funcionam da mesma forma, com o CNPJ validado e formatado." |

### Cena 7: Produtos (3:40 a 4:30)
| O que fazer na tela | O que falar |
|---|---|
| Menu **Produtos** → **Novo produto** → código `7891000100` (repetido), nome `Pão de Forma 500g`, categoria **Padaria**, custo `6,20`, venda `8,90`, mínimo `5` → **Salvar** | "Ao cadastrar um produto, o código precisa ser único…" |
| Mostre o erro → troque o código para `7891002000` → **Salvar** | "…corrijo o código e salvo. Repare que não existe campo de quantidade: o estoque só muda por entradas e saídas, para manter o histórico confiável." |
| Na lista, digite `café` na pesquisa → **Buscar**; depois limpe e escolha **Estoque baixo** → **Buscar** | "Também é possível pesquisar por nome ou código e filtrar só os produtos com estoque baixo." |

### Cena 8: Entradas e saídas, a funcionalidade principal (4:30 a 5:40)
| O que fazer na tela | O que falar |
|---|---|
| Menu **Movimentações** → **Nova entrada** → produto **Pão de Forma 500g** → quantidade `10` → observação `Compra NF 100` → **Registrar entrada** | "Agora a funcionalidade principal. Registro uma entrada de 10 unidades. Data, hora e usuário são gravados automaticamente." |
| **Nova saída** → **Pão de Forma 500g** → quantidade `50` → **Registrar saída** | "Se eu tentar tirar 50 unidades e só existem 10, o sistema **bloqueia** e informa quanto há disponível." |
| Corrija a quantidade para `6` → **Registrar saída** | "Com 6 unidades a saída é registrada, e o sistema avisa que o produto ficou com estoque baixo, já que o mínimo é 5." |
| No histórico, filtre por **Tipo: Saída** → **Filtrar** | "O histórico mostra todas as movimentações, com filtros por produto, tipo e período. Movimentações não podem ser alteradas nem excluídas: um erro é corrigido com uma movimentação inversa." |

### Cena 9: Tratamento de erros (5:40 a 6:05)
| O que fazer na tela | O que falar |
|---|---|
| Menu **Produtos** → **Excluir** no **Pão de Forma 500g** → confirme | "Outro exemplo de regra: um produto que já teve movimentações não pode ser excluído, para preservar o histórico." |
| Na barra de endereço, digite `https://estoquefacil-f1t6.onrender.com/pagina-inexistente` | "E se alguém acessar um endereço que não existe, aparece uma página de erro amigável, com o botão para voltar ao painel." |

### Cena 10: Testes automatizados (6:05 a 6:40)
| O que fazer na tela | O que falar |
|---|---|
| Explorador de Arquivos → pasta `ProjetoIntegrador` → duplo clique em **`rodar_testes.bat`**; espere o final | "A qualidade foi verificada com **testes automatizados em pytest**: são 152 testes cobrindo as regras de negócio, as telas e os cadastros. Todos passando." |

### Cena 11: Encerramento (6:40 a 7:00)
| O que fazer na tela | O que falar |
|---|---|
| Volte ao painel do sistema | "Esse foi o EstoqueFácil. O link do sistema, o código e toda a documentação estão no repositório do GitHub. Obrigado!" |

---

## Gravar com o Clipchamp (já vem no Windows 11)

1. Menu Iniciar → digite **Clipchamp** → abra.
2. **Criar um novo vídeo** → na lateral, **Gravar e criar** → **Gravação de tela**
   (ou **Tela e câmera**, se quiser aparecer no canto).
3. Escolha **compartilhar a janela do navegador** (ou a tela inteira, para mostrar também o Explorador de Arquivos na cena 10).
4. Confira se o **microfone** está ativado → **Gravar**. Siga o roteiro.
5. Ao terminar → **Salvar e editar**. Se quiser, corte começo e fim (arraste as bordas do clipe na linha do tempo).
6. **Confira a duração:** precisa ter **5 minutos ou mais**.
7. **Exportar** → **1080p** → salve o arquivo `.mp4`.

> 🔁 **Vai regravar do zero?** A gravação anterior já cadastrou "Padaria" e o código `7891002000`, então o sistema
> vai recusá-los (corretamente). Use outros valores (ex.: categoria `Padaria e Confeitaria`, produto `Pão Integral 500g`,
> código `7891002001`) ou peça ao Claude para restaurar os dados de exemplo.
>
> 💡 Errou no meio? Não pare a gravação: respire, volte ao último ponto e repita a frase. Depois corte o trecho
> no Clipchamp (posicione a agulha, clique na tesoura e apague o pedaço).

## Publicar no YouTube

1. Acesse https://studio.youtube.com (entre com sua conta Google).
2. **Criar → Enviar vídeos** → selecione o `.mp4`.
3. **Título:** `EstoqueFácil – PIT Engenharia de Software II – Demonstração`
4. **Descrição** (copie e cole):
   ```
   Projeto Integrador Transdisciplinar em Engenharia de Software II
   Aluno: Carlos Vinicius Oliveira de Pontes – RGM 40631559
   Sistema: https://estoquefacil-f1t6.onrender.com
   Código e documentação: https://github.com/Carlosvpontes/ProjetoIntegrador
   ```
5. Em "Público-alvo", marque **Não é conteúdo para crianças** → **Avançar** até **Visibilidade**.
6. Escolha **Não listado** (só quem tem o link assiste) → **Salvar**.
7. **Copie o link** e teste-o numa aba anônima.

✅ **Depois:** envie o link ao Claude ("o link do vídeo 1 é …"). Ele registra o link no README, no roadmap e no `PIT_atividade.docx`.
