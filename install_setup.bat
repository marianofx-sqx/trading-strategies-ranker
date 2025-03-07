@echo off
setlocal EnableDelayedExpansion

echo Instalando y configurando el Ranker de Estrategias de Trading...
echo ==================================================

echo 1. Verificando si Python esta instalado...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta instalado. Descargando e instalando Python 3.11...
    start /wait "" https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Error al instalar Python. Por favor, instala manualmente desde https://python.org y reinicia este script.
        pause
        exit /b 1
    )
) else (
    echo Python ya esta instalado. Version: !python --version!
)

echo 2. Instalando las bibliotecas necesarias...
python -m pip install --upgrade pip
pip install pandas matplotlib numpy streamlit
if %errorlevel% neq 0 (
    echo Error al instalar las bibliotecas. Verifica tu conexion a internet y permisos.
    pause
    exit /b 1
)

echo 3. Verificando y configurando la carpeta C:\ESTRATEGIAS_RANKING...
if exist "C:\ESTRATEGIAS_RANKING" (
    echo La carpeta C:\ESTRATEGIAS_RANKING ya existe.
    set /p choice="¿Deseas usar la carpeta existente (S) o crear una nueva eliminando el contenido actual (N)? [S/N]: "
    if /i "!choice!"=="N" (
        rmdir /S /Q "C:\ESTRATEGIAS_RANKING"
        mkdir "C:\ESTRATEGIAS_RANKING"
        echo Carpeta creada de nuevo.
    ) else (
        echo Usando la carpeta existente.
    )
) else (
    mkdir "C:\ESTRATEGIAS_RANKING"
    echo Carpeta C:\ESTRATEGIAS_RANKING creada con exito.
)

echo 4. Descargando los scripts necesarios...
for %%F in (dashboard.py rankear_estrategias.py) do (
    set "file=C:\ESTRATEGIAS_RANKING\%%F"
    if exist "!file!" (
        set /p overwrite="El archivo !file! ya existe. ¿Deseas sobrescribirlo? (S/N): "
        if /i "!overwrite!"=="S" (
            curl -o "!file!" "https://raw.githubusercontent.com/marianofx-sqx/trading-strategies-ranker/main/%%F"
            if !errorlevel! neq 0 (
                echo Error al descargar !file!. Verifica tu conexion a internet.
                pause
                exit /b 1
            ) else (
                echo !file! descargado con exito.
            )
        ) else (
            echo Manteniendo el archivo existente !file!.
        )
    ) else (
        curl -o "!file!" "https://raw.githubusercontent.com/marianofx-sqx/trading-strategies-ranker/main/%%F"
        if !erro