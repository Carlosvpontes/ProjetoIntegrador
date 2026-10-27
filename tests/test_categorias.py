"""Testes do cadastro de categorias (RF03, RN06)."""
import html

from sqlalchemy import select

from app.extensions import db
from app.models import Categoria


def _texto(resposta):
    """HTML da resposta com as entidades convertidas (&#34; vira "), como o navegador exibe."""
    return html.unescape(resposta.get_data(as_text=True))


def test_lista_exige_login(client):
    assert client.get("/categorias/").status_code == 302


def test_lista_vazia(cliente_logado):
    texto = _texto(cliente_logado.get("/categorias/"))
    assert "Nova categoria" in texto
    assert "Nenhum registro encontrado." in texto


def test_incluir_categoria(cliente_logado):
    resposta = cliente_logado.post(
        "/categorias/nova", data={"nome": "  Bebidas ", "descricao": "Sucos e refrigerantes"}, follow_redirects=True
    )
    assert "Categoria cadastrada com sucesso." in _texto(resposta)  # M04
    categoria = db.session.scalar(select(Categoria))
    assert categoria.nome == "Bebidas"
    assert categoria.descricao == "Sucos e refrigerantes"


def test_incluir_sem_nome_mostra_erro(cliente_logado):
    resposta = cliente_logado.post("/categorias/nova", data={"nome": ""}, follow_redirects=True)
    texto = _texto(resposta)
    assert "Informe o nome da categoria" in texto
    assert "Corrija os campos destacados." in texto
    assert db.session.scalar(select(Categoria)) is None


def test_nome_repetido_ignorando_maiusculas(cliente_logado, categoria):
    resposta = cliente_logado.post("/categorias/nova", data={"nome": "ALIMENTOS"}, follow_redirects=True)
    assert "Já existe uma categoria com esse nome." in _texto(resposta)  # M32


def test_editar_categoria(cliente_logado, categoria):
    tela = _texto(cliente_logado.get(f"/categorias/{categoria.id}/editar"))
    assert 'value="Alimentos"' in tela

    resposta = cliente_logado.post(
        f"/categorias/{categoria.id}/editar", data={"nome": "Mercearia", "descricao": ""}, follow_redirects=True
    )
    assert "Categoria atualizada com sucesso." in _texto(resposta)  # M05
    assert categoria.nome == "Mercearia"
    assert categoria.descricao is None


def test_editar_mantendo_o_proprio_nome(cliente_logado, categoria):
    resposta = cliente_logado.post(f"/categorias/{categoria.id}/editar", data={"nome": "Alimentos"}, follow_redirects=True)
    assert "Categoria atualizada com sucesso." in _texto(resposta)


def test_excluir_categoria_sem_produtos(cliente_logado, categoria):
    resposta = cliente_logado.post(f"/categorias/{categoria.id}/excluir", follow_redirects=True)
    assert 'Categoria "Alimentos" excluída com sucesso.' in _texto(resposta)  # M06
    assert db.session.scalar(select(Categoria)) is None


def test_nao_exclui_categoria_com_produtos(cliente_logado, categoria, produto):
    resposta = cliente_logado.post(f"/categorias/{categoria.id}/excluir", follow_redirects=True)
    assert "Não é possível excluir: existem 1 produto(s) vinculado(s)." in _texto(resposta)  # M27 / RN06
    assert db.session.get(Categoria, categoria.id) is not None


def test_categoria_inexistente_retorna_404(cliente_logado):
    assert cliente_logado.get("/categorias/999/editar").status_code == 404


def test_excluir_exige_post(cliente_logado, categoria):
    assert cliente_logado.get(f"/categorias/{categoria.id}/excluir").status_code == 405
