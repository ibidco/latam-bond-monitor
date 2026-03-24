@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 ACTUALIZADOR DE DATOS - MONITOR DE BONOS LATAM
echo    Con histórico de precios
echo ============================================================
echo.

REM Verificar si existe el archivo Excel
if not exist "Monitor_de_spreads.xlsx" (
    echo ❌ Error: No se encuentra el archivo Monitor_de_spreads.xlsx
    echo.
    echo Por favor, coloca tu archivo Excel en esta carpeta y
    echo asegúrate de que se llame "Monitor_de_spreads.xlsx"
    echo.
    pause
    exit /b 1
)

REM Ejecutar el script Python
echo 📊 Actualizando datos y guardando histórico...
echo.
python update_bond_data.py Monitor_de_spreads.xlsx

if errorlevel 1 (
    echo.
    echo ❌ Hubo un error al actualizar los datos
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 📤 SUBIENDO CAMBIOS A GITHUB...
echo ============================================================
echo.

REM Agregar cambios (incluye historical_data.json)
git add index.html historical_data.json
if errorlevel 1 (
    echo ❌ Error: Git no está configurado o no estás en un repositorio
    pause
    exit /b 1
)

REM Hacer commit
git commit -m "Actualizar datos de bonos con histórico - %date%"

REM Push a GitHub
echo.
echo 🌐 Subiendo a GitHub...
git push

if errorlevel 1 (
    echo.
    echo ❌ Error al subir a GitHub
    echo Verifica tu conexión y permisos
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ ¡TODO LISTO!
echo ============================================================
echo.
echo ✅ Datos actualizados con histórico de precios
echo ✅ Tu sitio se actualizará en Vercel en ~30 segundos
echo.
echo URL de tu sitio: https://tu-sitio.vercel.app
echo.
pause
