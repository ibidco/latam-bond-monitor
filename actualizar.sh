#!/bin/bash

echo "============================================================"
echo "🚀 ACTUALIZADOR DE DATOS - MONITOR DE BONOS LATAM"
echo "   Con histórico de precios"
echo "============================================================"
echo ""

# Verificar si existe el archivo Excel
if [ ! -f "Monitor_de_spreads.xlsx" ]; then
    echo "❌ Error: No se encuentra el archivo Monitor_de_spreads.xlsx"
    echo ""
    echo "Por favor, coloca tu archivo Excel en esta carpeta y"
    echo "asegúrate de que se llame 'Monitor_de_spreads.xlsx'"
    echo ""
    exit 1
fi

# Ejecutar el script Python
echo "📊 Actualizando datos y guardando histórico..."
echo ""
python3 update_bond_data.py Monitor_de_spreads.xlsx

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Hubo un error al actualizar los datos"
    echo ""
    exit 1
fi

echo ""
echo "============================================================"
echo "📤 SUBIENDO CAMBIOS A GITHUB..."
echo "============================================================"
echo ""

# Agregar cambios (incluye historical_data.json)
git add index.html historical_data.json
if [ $? -ne 0 ]; then
    echo "❌ Error: Git no está configurado o no estás en un repositorio"
    exit 1
fi

# Hacer commit
git commit -m "Actualizar datos de bonos con histórico - $(date +%Y-%m-%d)"

# Push a GitHub
echo ""
echo "🌐 Subiendo a GitHub..."
git push

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error al subir a GitHub"
    echo "Verifica tu conexión y permisos"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ ¡TODO LISTO!"
echo "============================================================"
echo ""
echo "✅ Datos actualizados con histórico de precios"
echo "✅ Tu sitio se actualizará en Vercel en ~30 segundos"
echo ""
echo "URL de tu sitio: https://tu-sitio.vercel.app"
echo ""
