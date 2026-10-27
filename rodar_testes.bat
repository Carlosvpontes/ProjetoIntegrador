@echo off
chcp 65001 >nul
title EstoqueFacil - testes automatizados
cd /d "%~dp0"

if not exist .venv\Scripts\python.exe (
    echo Criando o ambiente do projeto pela primeira vez...
    py -3 -m venv .venv || goto erro
)

echo Verificando bibliotecas...
.venv\Scripts\python.exe -m pip install --disable-pip-version-check -q -r requirements.txt || goto erro

echo.
echo Executando os testes automatizados...
echo.
.venv\Scripts\python.exe -m pytest -v
echo.
pause
exit /b 0

:erro
echo.
echo *** Ocorreu um erro. Copie a mensagem acima e envie ao Claude. ***
pause
exit /b 1
