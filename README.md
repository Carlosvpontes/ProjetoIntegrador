# EstoqueFácil: Controle de Estoque para Pequenos Comércios

**Projeto Integrador Transdisciplinar em Engenharia de Software II**

> 🚧 **Em desenvolvimento**

**Autor:** [@Carlosvpontes](https://github.com/Carlosvpontes)

## Sobre o projeto

Pequenos comércios costumam controlar o estoque em cadernos ou planilhas, o que causa falta de
produtos, compras desnecessárias e nenhum histórico de quem retirou ou repôs mercadoria.

O **EstoqueFácil** é um sistema web simples para o comerciante saber, a qualquer momento,
**o que tem, quanto tem e o que precisa repor**:

- Cadastro de produtos, categorias e fornecedores;
- Registro de entradas e saídas de mercadoria, com data, hora e responsável;
- Bloqueio de saídas maiores que o estoque disponível;
- Alerta automático de produtos com estoque baixo;
- Painel com a situação geral do estoque.

![Painel do EstoqueFácil (protótipo)](docs/situacao-1/prototipo/prints/t03-painel.png)

📄 Documentação completa do planejamento: [docs/situacao-1](docs/situacao-1/README.md)

## Links

| Item | Link |
|---|---|
| Sistema em funcionamento | _a definir_ |
| Vídeo de demonstração (narrado) | _a definir_ |
| Vídeo da solução atualizada | _a definir_ |

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3 + Flask (arquitetura MVC) |
| Front-end | HTML5, CSS3 (Bootstrap), JavaScript |
| Banco de dados | MySQL (produção) / SQLite (desenvolvimento local) |
| Testes | pytest |
| Hospedagem | PythonAnywhere |
| Modo de codificação | Tradicional |

## Estrutura do repositório

```
ProjetoIntegrador/
├── docs/
│   ├── situacao-1/   → Documentação revisada: escopo, requisitos, UML, IHC, banco de dados
│   ├── situacao-2/   → Manual de uso e evidências dos testes automatizados
│   └── situacao-3/   → Plano de testes, avaliações dos testadores e laudo de qualidade
├── database/         → Projeto físico do banco de dados (schema.sql)
├── app/              → Código-fonte (Model, View, Controller)
└── tests/            → Testes automatizados
```

## Andamento

- [ ] **Situação 1:** Documentação revisada
- [ ] **Situação 2:** Codificação (front-end, back-end, testes, publicação)
- [ ] **Situação 3:** Testes com usuários, correções e laudo de qualidade
