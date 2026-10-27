@echo off
chcp 65001 >nul
title EstoqueFacil - servidor local
cd /d "%~dp0"

if not exist .venv\Scripts\python.exe (
    echo Criando o ambiente do projeto pela primeira vez...
    py -3 -m venv .venv || goto erro
)

echo Verificando bibliotecas...
.venv\Scripts\python.exe -m pip install --disable-pip-version-check -q -r requirements.txt || goto erro

if not exist instance\estoque.db (
    echo Criando o banco de dados com dados de exemplo...
    .venv\Scripts\python.exe criar_banco.py --exemplo || goto erro
)

echo.
echo ============================================================
echo   EstoqueFacil rodando em: http://127.0.0.1:5000
echo   Login de exemplo: demo@estoquefacil.com / senha demo123
echo   Para PARAR o sistema, feche esta janela.
echo ============================================================
echo.
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
.venv\Scripts\python.exe run.py
pause
exit /b 0

:erro
echo.
echo *** Ocorreu um erro. Copie a mensagem acima e envie ao Claude. ***
pause
exit /b 1
