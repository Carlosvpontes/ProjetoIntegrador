# Conteúdo do arquivo WSGI do PythonAnywhere (aba Web → "WSGI configuration file").
# Apague tudo o que estiver lá e cole este texto. Não há senhas aqui: elas ficam no .env.
import sys

PASTA_PROJETO = "/home/carlosvpontes/ProjetoIntegrador"
if PASTA_PROJETO not in sys.path:
    sys.path.insert(0, PASTA_PROJETO)

from run import app as application  # noqa: E402,F401
