"""Testes do cadastro e da pesquisa de produtos (RF05, RF10, RF11, RN03, RN05, RN07, RN12)."""
import html
from decimal import Decimal

from sqlalchemy import select

from app.extensions import db
from app.models import Categoria, Produto


def _texto(resposta):
    """HTML da resposta com as entidades convertidas (&#34; vira "), como o navegador exibe."""
    return html.unescape(resposta.get_data(as_text=True))


def _dados(categoria, **alteracoes):
    dados = {
        "codigo": "7891000300",
        "nome": "Refrigerante 2L",
        "descricao": "",
        "categoria_id": str(categoria.id),
        "fornecedor_id": "",
        "preco_custo": "6,80",
        "preco_venda": "9,99",
        "estoque_minimo": "12",
    }
    dados.update(alteracoes)
    return dados


def _novo(client, categoria, **alteracoes):
    return client.post("/produtos/novo", data=_dados(categoria, **alteracoes), follow_redirects=True)


# ---------- Incluir ----------

def test_lista_exige_login(client):
    assert client.get("/produtos/").status_code == 302


def test_incluir_produto(cliente_logado, categoria, fornecedor):
    resposta = _novo(cliente_logado, categoria, fornecedor_id=str(fornecedor.id))
    assert "Produto cadastrado com sucesso." in _texto(resposta)  # M04

    produto = db.session.scalar(select(Produto))
    assert produto.nome == "Refrigerante 2L"
    assert produto.preco_custo == Decimal("6.80")
    assert produto.preco_venda == Decimal("9.99")
    assert produto.estoque_minimo == 12
    assert produto.fornecedor == fornecedor
    assert produto.quantidade_atual == 0  # RN03


def test_formulario_nao_altera_quantidade_em_estoque(cliente_logado, categoria):
    """RN03: mesmo que alguém envie o campo, a quantidade não muda pelo formulário."""
    _novo(cliente_logado, categoria, quantidade_atual="500")
    assert db.session.scalar(select(Produto)).quantidade_atual == 0


def test_campos_obrigatorios(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, codigo="", nome="", categoria_id="")
    texto = _texto(resposta)
    assert "Informe o código" in texto
    assert "Informe o nome do produto" in texto
    assert "Selecione uma categoria." in texto
    assert db.session.scalar(select(Produto)) is None


def test_codigo_repetido(cliente_logado, categoria, produto):
    resposta = _novo(cliente_logado, categoria, codigo="p001")
    assert 'Já existe um produto com o código "p001".' in _texto(resposta)  # M26 / RN05


def test_codigo_com_caracteres_invalidos(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, codigo="ABC 123!")
    assert "letras, números ou hífen" in _texto(resposta)


def test_preco_negativo(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, preco_venda="-1")
    assert "O valor não pode ser negativo." in _texto(resposta)  # M30 / RN12


def test_estoque_minimo_invalido(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, estoque_minimo="dez")
    assert "Informe um número inteiro igual ou maior que zero." in _texto(resposta)


def test_categoria_inexistente(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, categoria_id="999")
    assert "Selecione uma categoria." in _texto(resposta)


def test_formulario_avisa_quando_nao_ha_categorias(cliente_logado):
    assert "é preciso ter pelo menos uma categoria" in _texto(cliente_logado.get("/produtos/novo"))


def test_erro_mantem_os_dados_digitados(cliente_logado, categoria):
    resposta = _novo(cliente_logado, categoria, nome="", preco_custo="6,80")
    assert 'value="6,80"' in _texto(resposta)


# ---------- Editar ----------

def test_tela_de_edicao_mostra_valores_e_estoque_atual(cliente_logado, produto, usuario):
    produto.registrar_entrada(8, usuario)
    db.session.commit()

    texto = _texto(cliente_logado.get(f"/produtos/{produto.id}/editar"))
    assert 'value="20,00"' in texto
    assert "Estoque atual: <strong>8 unidade(s)</strong>" in texto


def test_editar_produto(cliente_logado, categoria, produto):
    resposta = cliente_logado.post(
        f"/produtos/{produto.id}/editar",
        data=_dados(categoria, codigo="P001", nome="Arroz Tipo 1 5kg", preco_venda="29,90"),
        follow_redirects=True,
    )
    assert "Produto atualizado com sucesso." in _texto(resposta)  # M05
    assert produto.nome == "Arroz Tipo 1 5kg"
    assert produto.preco_venda == Decimal("29.90")


# ---------- Excluir ----------

def test_excluir_produto_sem_movimentacoes(cliente_logado, produto):
    resposta = cliente_logado.post(f"/produtos/{produto.id}/excluir", follow_redirects=True)
    assert 'Produto "Arroz 5kg" excluído com sucesso.' in _texto(resposta)  # M06
    assert db.session.scalar(select(Produto)) is None


def test_nao_exclui_produto_com_movimentacoes(cliente_logado, produto, usuario):
    produto.registrar_entrada(1, usuario)
    db.session.commit()

    resposta = cliente_logado.post(f"/produtos/{produto.id}/excluir", follow_redirects=True)
    assert "este produto possui movimentações" in _texto(resposta)  # M28 / RN07
    assert db.session.get(Produto, produto.id) is not None


# ---------- Pesquisa e filtros (RF10, RF11) ----------

def _cadastrar_varios(categoria, usuario):
    bebidas = Categoria(nome="Bebidas")
    arroz = Produto(codigo="A1", nome="Arroz", categoria=categoria, estoque_minimo=5)
    feijao = Produto(codigo="F1", nome="Feijão", categoria=categoria, estoque_minimo=5)
    suco = Produto(codigo="S1", nome="Suco 50% fruta", categoria=bebidas, estoque_minimo=0)
    db.session.add_all([bebidas, arroz, feijao, suco])
    arroz.registrar_entrada(50, usuario)  # acima do mínimo
    feijao.registrar_entrada(2, usuario)  # estoque baixo
    suco.registrar_entrada(10, usuario)
    db.session.commit()
    return bebidas


def _nomes_na_tabela(texto):
    return {nome for nome in ["Arroz", "Feijão", "Suco 50% fruta"] if f"<td>{nome}" in texto}


def test_lista_todos_os_produtos(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    texto = _texto(cliente_logado.get("/produtos/"))
    assert _nomes_na_tabela(texto) == {"Arroz", "Feijão", "Suco 50% fruta"}
    assert "Estoque baixo</span>" in texto


def test_pesquisa_por_nome_sem_diferenciar_maiusculas(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    assert _nomes_na_tabela(_texto(cliente_logado.get("/produtos/?q=arr"))) == {"Arroz"}


def test_pesquisa_por_codigo(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    assert _nomes_na_tabela(_texto(cliente_logado.get("/produtos/?q=F1"))) == {"Feijão"}


def test_pesquisa_com_porcentagem_e_tratada_como_texto(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    assert _nomes_na_tabela(_texto(cliente_logado.get("/produtos/?q=50%25"))) == {"Suco 50% fruta"}


def test_filtro_por_categoria(cliente_logado, categoria, usuario):
    bebidas = _cadastrar_varios(categoria, usuario)
    assert _nomes_na_tabela(_texto(cliente_logado.get(f"/produtos/?categoria={bebidas.id}"))) == {"Suco 50% fruta"}


def test_filtro_estoque_baixo(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    assert _nomes_na_tabela(_texto(cliente_logado.get("/produtos/?situacao=baixo"))) == {"Feijão"}


def test_pesquisa_sem_resultado(cliente_logado, categoria, usuario):
    _cadastrar_varios(categoria, usuario)
    assert "Nenhum registro encontrado." in _texto(cliente_logado.get("/produtos/?q=xyz"))  # M51
