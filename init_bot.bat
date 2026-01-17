@echo off
title Cargando el Bot de Trading...
echo --------------------------------------------------
echo Preparando el entorno... (Esto solo tarda la primera vez)
echo --------------------------------------------------

:: Comprobar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: No tienes Python instalado. 
    echo Por favor, instala Python desde python.org y vuelve a intentarlo.
    pause
    exit
)

:: Instalar librerias silenciosamente
pip install -r requirements.txt --quiet

echo --------------------------------------------------
echo TODO LISTO. Abriendo la interfaz en tu navegador...
echo --------------------------------------------------

:: Ejecutar streamlit
streamlit run app.py

pause