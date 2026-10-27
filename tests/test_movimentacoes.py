"""Testes de entradas, saídas e histórico (RF06, RF07, RF08, RN01, RN02, RN10, RN11)."""
import html
from datetime import timedelta

from sqlalchemy import func, select

from app.extensions import db
from app.models import Movimentacao, Produto, TipoMovimentacao
from app.models.base import agora


def _texto(resposta):
    """HTML da resposta com as entidades convertidas (&#34; vira "), como o navegador exibe."""
    return html.unescape(resposta.get_data(as_text=True))


def _registrar(client, tipo, produto, quantidade, observacao=""):
    return client.post(
        f"/movimentacoes/nova/{tipo}",
        data={"produto_id": str(produto.id), "quantidade": str(quantidade), "observacao": observacao},
        follow_redirects=True,
    )


def _total_movimentacoes():
    return db.session.scalar(select(func.count(Movimentacao.id)))


# ---------- Acesso ----------

def test_telas_exigem_login(client):
    assert client.get("/movimentacoes/").status_code == 302
    assert client.get("/movimentacoes/nova/entrada").status_code == 302


def test_tipo_invalido_na_url_retorna_404(cliente_logado):
    assert cliente_logado.get("/movimentacoes/nova/transferencia").status_code == 404


def test_formulario_lista_produtos_com_estoque(cliente_logado, produto, usuario):
    produto.registrar_entrada(7, usuario)
    db.session.commit()
    texto = _texto(cliente_logado.get("/movimentacoes/nova/saida"))
    assert "Registrar saída" in texto
    assert "Arroz 5kg — P001 (estoque: 7)" in texto


def test_formulario_ja_vem_com_produto_selecionado(cliente_logado, produto):
    texto = _texto(cliente_logado.get(f"/movimentacoes/nova/entrada?produto={produto.id}"))
    assert f'<option value="{produto.id}" selected>' in texto


def test_formulario_avisa_quando_nao_ha_produtos(cliente_logado):
    assert "Nenhum produto cadastrado." in _texto(cliente_logado.get("/movimentacoes/nova/entrada"))


# ---------- Entrada (RF06) ----------

def test_registrar_entrada(cliente_logado, produto, usuario):
    resposta = _registrar(cliente_logado, "entrada", produto, 10, "Compra NF 123")

    assert 'Entrada de 10 unidade(s) de "Arroz 5kg" registrada.' in _texto(resposta)  # M11
    assert produto.quantidade_atual == 10
    mov = db.session.scalar(select(Movimentacao))
    assert mov.tipo == TipoMovimentacao.ENTRADA
    assert mov.observacao == "Compra NF 123"
    assert mov.usuario_id == usuario.id  # RN10
    assert "Compra NF 123" in _texto(resposta)  # aparece no histórico


# ---------- Saída (RF07) ----------

def test_registrar_saida(cliente_logado, produto, usuario):
    produto.registrar_entrada(20, usuario)
    db.session.commit()

    resposta = _registrar(cliente_logado, "saida", produto, 8, "Venda balcão")
    assert 'Saída de 8 unidade(s) de "Arroz 5kg" registrada.' in _texto(resposta)  # M10
    assert produto.quantidade_atual == 12


def test_saida_maior_que_estoque_e_bloqueada(cliente_logado, produto, usuario):
    produto.registrar_entrada(2, usuario)
    db.session.commit()

    resposta = _registrar(cliente_logado, "saida", produto, 5)
    texto = _texto(resposta)
    assert 'Estoque insuficiente: há apenas 2 unidade(s) de "Arroz 5kg".' in texto  # M21 / RN01
    assert "Máximo disponível: 2" in texto
    assert 'value="5"' in texto  # mantém o que foi digitado
    assert produto.quantidade_atual == 2
    assert _total_movimentacoes() == 1  # apenas a entrada inicial


def test_saida_que_deixa_estoque_baixo_mostra_aviso(cliente_logado, produto, usuario):
    produto.registrar_entrada(10, usuario)  # mínimo do produto = 5
    db.session.commit()

    resposta = _registrar(cliente_logado, "saida", produto, 6)
    assert 'Atenção: "Arroz 5kg" está com estoque baixo (4 unidade(s)).' in _texto(resposta)  # M52


def test_saida_que_mantem_estoque_acima_do_minimo_nao_mostra_aviso(cliente_logado, produto, usuario):
    produto.registrar_entrada(10, usuario)
    db.session.commit()
    assert "estoque baixo (" not in _texto(_registrar(cliente_logado, "saida", produto, 1))


# ---------- Validações (RN02) ----------

def test_quantidade_invalida(cliente_logado, produto):
    for quantidade in ["0", "-3", "2,5", "abc", ""]:
        resposta = _registrar(cliente_logado, "entrada", produto, quantidade)
        assert "Informe uma quantidade inteira maior que zero." in _texto(resposta)  # M20
    assert _total_movimentacoes() == 0
    assert produto.quantidade_atual == 0


def test_produto_nao_selecionado(cliente_logado, produto):
    resposta = cliente_logado.post(
        "/movimentacoes/nova/entrada", data={"produto_id": "", "quantidade": "3"}, follow_redirects=True
    )
    assert "Selecione um produto." in _texto(resposta)
    assert _total_movimentacoes() == 0


def test_produto_inexistente(cliente_logado, produto):
    resposta = cliente_logado.post(
        "/movimentacoes/nova/entrada", data={"produto_id": "999", "quantidade": "3"}, follow_redirects=True
    )
    assert "Selecione um produto." in _texto(resposta)


# ---------- Histórico (RF08) e imutabilidade (RN11) ----------

def _criar_historico(produto, categoria, usuario):
    feijao = Produto(codigo="F1", nome="Feijão", categoria=categoria)
    db.session.add(feijao)
    antiga = produto.registrar_entrada(30, usuario, "entrada antiga")
    antiga.data_hora = agora() - timedelta(days=60)
    produto.registrar_saida(5, usuario, "saida de hoje")
    feijao.registrar_entrada(9, usuario, "feijao de hoje")
    db.session.commit()
    return feijao


def test_historico_padrao_mostra_ultimos_30_dias(cliente_logado, produto, categoria, usuario):
    _criar_historico(produto, categoria, usuario)
    texto = _texto(cliente_logado.get("/movimentacoes/"))
    assert "saida de hoje" in texto
    assert "feijao de hoje" in texto
    assert "entrada antiga" not in texto
    assert "2 movimentação(ões) exibida(s)." in texto


def test_historico_sem_datas_mostra_tudo(cliente_logado, produto, categoria, usuario):
    _criar_historico(produto, categoria, usuario)
    texto = _texto(cliente_logado.get("/movimentacoes/?inicio=&fim="))
    assert "entrada antiga" in texto
    assert "3 movimentação(ões) exibida(s)." in texto


def test_historico_filtra_por_produto(cliente_logado, produto, categoria, usuario):
    feijao = _criar_historico(produto, categoria, usuario)
    texto = _texto(cliente_logado.get(f"/movimentacoes/?produto={feijao.id}&inicio=&fim="))
    assert "feijao de hoje" in texto
    assert "saida de hoje" not in texto


def test_historico_filtra_por_tipo(cliente_logado, produto, categoria, usuario):
    _criar_historico(produto, categoria, usuario)
    texto = _texto(cliente_logado.get("/movimentacoes/?tipo=SAIDA&inicio=&fim="))
    assert "saida de hoje" in texto
    assert "feijao de hoje" not in texto
    assert "entrada antiga" not in texto


def test_historico_filtra_por_periodo_incluindo_o_ultimo_dia(cliente_logado, produto, categoria, usuario):
    _criar_historico(produto, categoria, usuario)
    dia_antigo = (agora() - timedelta(days=60)).date().isoformat()
    texto = _texto(cliente_logado.get(f"/movimentacoes/?inicio={dia_antigo}&fim={dia_antigo}"))
    assert "entrada antiga" in texto
    assert "saida de hoje" not in texto


def test_historico_vazio(cliente_logado):
    assert "Nenhum registro encontrado." in _texto(cliente_logado.get("/movimentacoes/"))  # M51


def test_movimentacoes_nao_podem_ser_editadas_nem_excluidas(cliente_logado, produto, usuario):
    """RN11: não existem rotas de edição ou exclusão de movimentações."""
    mov = produto.registrar_entrada(1, usuario)
    db.session.commit()
    assert cliente_logado.get(f"/movimentacoes/{mov.id}/editar").status_code == 404
    assert cliente_logado.post(f"/movimentacoes/{mov.id}/excluir").status_code == 404


# ---------- Integração com o painel ----------

def test_painel_reflete_movimentacoes(cliente_logado, produto):
    _registrar(cliente_logado, "entrada", produto, 3)
    texto = _texto(cliente_logado.get("/"))
    assert "R$ 60,00" in texto  # 3 x R$ 20,00
    assert "1 produto(s) com estoque baixo." in texto
    assert "Nova entrada" in texto
