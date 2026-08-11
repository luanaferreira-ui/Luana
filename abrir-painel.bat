@echo off
REM Atalho para abrir o Painel de Demandas no Windows.
REM Dois cliques neste arquivo: sincroniza (git pull + caixa do radar),
REM sobe o servidor local e abre o navegador em http://localhost:4321.
cd /d "%~dp0"
echo Sincronizando e subindo o painel...
REM abre o navegador depois de 3s (dando tempo do servidor iniciar)
start "" cmd /c "timeout /t 3 >nul & start http://localhost:4321"
npm start
