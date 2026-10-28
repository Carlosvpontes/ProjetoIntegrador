"""Ponto de entrada do EstoqueFácil.

- No computador: python run.py (ou rodar_local.bat) → http://127.0.0.1:5000
- No Render: gunicorn run:app (definido em render.yaml)
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
