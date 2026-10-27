"""Testes de criar conta, entrar e sair (RF01, RF02, RN08, RN09)."""
from sqlalchemy import select

from app.extensions import db
from app.models import Usuario


def _cadastrar(client, **dados):
    formulario = {"nome": "Ana Souza", "email": "ana@email.com", "senha": "123456", "confirmacao": "123456"}
    formulario.update(dados)
    return client.post("/cadastro", data=formulario, follow_redirects=True)


def _texto(resposta):
    return resposta.get_data(as_text=True)


# ---------- Criar conta ----------

def test_tela_de_cadastro_abre(client):
    resposta = client.get("/cadastro")
    assert resposta.status_code == 200
    assert "Criar conta" in _texto(resposta)


def test_cadastro_com_sucesso(client):
    resposta = _cadastrar(client)
    assert "Conta criada com sucesso! Faça login para continuar." in _texto(resposta)  # M01
    usuario = db.session.scalar(select(Usuario).filter_by(email="ana@email.com"))
    assert usuario is not None
    assert usuario.verificar_senha("123456")


def test_email_e_guardado_em_minusculas(client):
    _cadastrar(client, email="  Ana@Email.COM ")
    assert db.session.scalar(select(Usuario).filter_by(email="ana@email.com")) is not None


def test_cadastro_com_email_repetido(client, usuario):
    resposta = _cadastrar(client, email=usuario.email)
    assert "Este e-mail já está cadastrado." in _texto(resposta)  # M23


def test_cadastro_com_senha_curta(client):
    resposta = _cadastrar(client, senha="123", confirmacao="123")
    assert "A senha deve ter no mínimo 6 caracteres." in _texto(resposta)  # M24
    assert db.session.scalar(select(Usuario).filter_by(email="ana@email.com")) is None


def test_cadastro_com_senhas_diferentes(client):
    resposta = _cadastrar(client, confirmacao="654321")
    assert "As senhas não conferem." in _texto(resposta)  # M25


def test_cadastro_com_dados_invalidos_mantem_o_que_foi_digitado(client):
    resposta = _cadastrar(client, nome="A", email="email-invalido")
    texto = _texto(resposta)
    assert "Informe seu nome" in texto
    assert "Informe um e-mail válido." in texto
    assert 'value="email-invalido"' in texto


# ---------- Entrar e sair ----------

def test_login_com_sucesso_vai_para_o_painel(client, usuario):
    resposta = client.post("/login", data={"email": usuario.email, "senha": "senha123"}, follow_redirects=True)
    texto = _texto(resposta)
    assert "Bem-vindo(a), Márcia Teste!" in texto  # M02
    assert "Painel" in texto


def test_login_com_senha_errada(client, usuario):
    resposta = client.post("/login", data={"email": usuario.email, "senha": "errada"}, follow_redirects=True)
    assert "E-mail ou senha incorretos." in _texto(resposta)  # M22


def test_login_com_email_inexistente(client):
    resposta = client.post("/login", data={"email": "ninguem@x.com", "senha": "123456"}, follow_redirects=True)
    assert "E-mail ou senha incorretos." in _texto(resposta)


def test_pagina_interna_exige_login(client):  # RN09
    resposta = client.get("/", follow_redirects=True)
    texto = _texto(resposta)
    assert "Faça login para acessar esta página." in texto  # M33
    assert "Entrar" in texto


def test_apos_login_volta_para_a_pagina_pedida(client, usuario):
    resposta = client.post("/login?next=/", data={"email": usuario.email, "senha": "senha123"})
    assert resposta.headers["Location"] == "/"


def test_login_nao_redireciona_para_outro_site(client, usuario):
    resposta = client.post(
        "/login?next=https://site-malicioso.com", data={"email": usuario.email, "senha": "senha123"}
    )
    assert resposta.headers["Location"] == "/"


def test_logout(cliente_logado):
    resposta = cliente_logado.post("/logout", follow_redirects=True)
    assert "Você saiu do sistema." in _texto(resposta)  # M03
    assert cliente_logado.get("/").status_code == 302  # voltou a exigir login
