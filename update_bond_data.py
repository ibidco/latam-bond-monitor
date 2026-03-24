#!/usr/bin/env python3
"""
Script para actualizar automáticamente los datos del Monitor de Bonos con histórico
Autor: Claude
Fecha: 2026-03-24

Uso:
    python update_bond_data.py path/to/Monitor_de_spreads.xlsx
"""

import pandas as pd
import json
import sys
import os
from datetime import datetime

def load_historical_data(history_file='historical_data.json'):
    """Carga el archivo de datos históricos si existe"""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  No se pudo cargar histórico: {e}")
            return {"snapshots": []}
    return {"snapshots": []}

def save_historical_snapshot(df, history_file='historical_data.json'):
    """Guarda un snapshot de los datos actuales en el histórico"""
    print("💾 Guardando snapshot histórico...")
    
    # Cargar histórico existente
    historical_data = load_historical_data(history_file)
    
    # Crear snapshot actual
    today = datetime.now()
    snapshot = {
        "date": today.strftime("%Y-%m-%d"),
        "timestamp": today.isoformat(),
        "bonds": {}
    }
    
    # Guardar solo Bond ID, Price, YTW, Spread para cada bono
    for _, row in df.iterrows():
        bond_id = row.get('Bond')
        if bond_id and pd.notna(bond_id):
            snapshot["bonds"][bond_id] = {
                "price": float(row['Price']) if pd.notna(row.get('Price')) else None,
                "ytw": float(row['YTW']) if pd.notna(row.get('YTW')) else None,
                "spread": float(row['Z sprd']) if pd.notna(row.get('Z sprd')) else None,
                "outstanding": float(row['Outstdng']) if pd.notna(row.get('Outstdng')) else None
            }
    
    # Agregar snapshot al histórico
    historical_data["snapshots"].append(snapshot)
    
    # Mantener solo últimos 90 días de datos (para no crecer infinitamente)
    cutoff_date = (today - pd.Timedelta(days=90)).strftime("%Y-%m-%d")
    historical_data["snapshots"] = [
        s for s in historical_data["snapshots"] 
        if s["date"] >= cutoff_date
    ]
    
    # Guardar archivo
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(historical_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Snapshot guardado. Total snapshots: {len(historical_data['snapshots'])}")
    return historical_data

def calculate_price_changes(df, historical_data):
    """Calcula cambios de precio vs. snapshots históricos"""
    if not historical_data["snapshots"]:
        print("⚠️  No hay datos históricos para calcular cambios")
        return df
    
    print("📊 Calculando cambios de precio...")
    
    today = datetime.now()
    snapshots = historical_data["snapshots"]
    
    # Encontrar snapshots de referencia (1 semana, 1 mes, 3 meses atrás)
    reference_dates = {
        "1w": (today - pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
        "1m": (today - pd.Timedelta(days=30)).strftime("%Y-%m-%d"),
        "3m": (today - pd.Timedelta(days=90)).strftime("%Y-%m-%d")
    }
    
    # Función para encontrar el snapshot más cercano a una fecha
    def find_closest_snapshot(target_date):
        closest = None
        min_diff = float('inf')
        for s in snapshots:
            diff = abs((datetime.fromisoformat(s["timestamp"]) - datetime.fromisoformat(target_date + "T00:00:00")).days)
            if diff < min_diff:
                min_diff = diff
                closest = s
        return closest if min_diff <= 7 else None  # Máximo 7 días de diferencia
    
    # Agregar columnas de cambio
    df['Price_1W'] = None
    df['Price_1M'] = None
    df['Price_3M'] = None
    
    for period, target_date in reference_dates.items():
        snapshot = find_closest_snapshot(target_date)
        if snapshot:
            col_name = f'Price_{period.upper()}'
            for idx, row in df.iterrows():
                bond_id = row['Bond']
                if bond_id in snapshot["bonds"]:
                    old_price = snapshot["bonds"][bond_id].get("price")
                    new_price = row.get('Price')
                    if old_price and new_price and pd.notna(new_price):
                        change = new_price - old_price
                        df.at[idx, col_name] = round(change, 2)
    
    return df

def excel_to_js_data(excel_path, include_historical=True):
    """Convierte el archivo Excel a formato JavaScript"""
    print(f"📖 Leyendo archivo Excel: {excel_path}")
    
    # Leer Excel
    df = pd.read_excel(excel_path)
    
    print(f"✅ Encontrados {len(df)} bonos")
    
    # Guardar snapshot histórico
    historical_data = None
    if include_historical:
        historical_data = save_historical_snapshot(df)
        df = calculate_price_changes(df, historical_data)
    
    # Convertir a lista de diccionarios
    bonds = df.to_dict('records')
    
    # Limpiar valores NaN y convertir a tipos apropiados
    cleaned_bonds = []
    for bond in bonds:
        cleaned_bond = {}
        for key, value in bond.items():
            if pd.isna(value):
                cleaned_bond[key] = None
            elif isinstance(value, (int, float)):
                cleaned_bond[key] = float(value) if value != int(value) else int(value)
            else:
                cleaned_bond[key] = str(value)
        cleaned_bonds.append(cleaned_bond)
    
    # Convertir a JavaScript
    js_data = "let bondsData = " + json.dumps(cleaned_bonds, indent=4) + ";"
    
    return js_data, len(cleaned_bonds), historical_data

def update_html_file(html_path, new_js_data):
    """Actualiza el archivo HTML con los nuevos datos"""
    print(f"🔧 Actualizando archivo HTML: {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Intentar encontrar bondsData con 'let' o 'const'
    start_marker_let = "let bondsData = ["
    start_marker_const = "const bondsData = ["
    end_marker = "];"
    
    # Buscar con 'let' primero
    start_idx = content.find(start_marker_let)
    if start_idx != -1:
        start_marker = start_marker_let
        # Cambiar el nuevo JS data para usar 'let' en vez de 'const'
        new_js_data = new_js_data.replace("const bondsData", "let bondsData")
    else:
        # Si no encuentra 'let', buscar con 'const'
        start_idx = content.find(start_marker_const)
        if start_idx != -1:
            start_marker = start_marker_const
        else:
            print("❌ Error: No se encontró 'let bondsData' ni 'const bondsData' en el HTML")
            return False
    
    # Encontrar el cierre del array
    bracket_count = 0
    i = start_idx + len(start_marker) - 1  # Posición del '['
    found_end = False
    
    while i < len(content):
        if content[i] == '[':
            bracket_count += 1
        elif content[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end_idx = i + 2  # Incluir '];'
                found_end = True
                break
        i += 1
    
    if not found_end:
        print("❌ Error: No se encontró el cierre de bondsData")
        return False
    
    # Reemplazar los datos
    new_content = content[:start_idx] + new_js_data + content[end_idx:]
    
    # Guardar archivo actualizado
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Archivo HTML actualizado exitosamente")
    return True

def update_date_in_html(html_path):
    """Actualiza la fecha 'Data as of' en el HTML"""
    print("📅 Actualizando fecha de corte...")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Obtener fecha actual
    today = datetime.now()
    new_date = today.strftime("%b %d, %Y")  # Formato: Feb 13, 2026
    
    # Buscar y reemplazar la fecha
    import re
    pattern = r'<span class="stat-value">[A-Za-z]{3} \d{1,2}, \d{4}</span>'
    replacement = f'<span class="stat-value">{new_date}</span>'
    
    # Solo reemplazar la última ocurrencia (que es la fecha "Data as of")
    matches = list(re.finditer(pattern, content))
    if matches:
        last_match = matches[-1]
        new_content = content[:last_match.start()] + replacement + content[last_match.end():]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Fecha actualizada a: {new_date}")
    else:
        print("⚠️  No se pudo actualizar la fecha automáticamente")

def main():
    print("=" * 60)
    print("🚀 ACTUALIZADOR DE DATOS - MONITOR DE BONOS LATAM")
    print("   Con seguimiento histórico de precios")
    print("=" * 60)
    print()
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("❌ Error: Debes proporcionar la ruta al archivo Excel")
        print()
        print("Uso:")
        print("    python update_bond_data.py Monitor_de_spreads.xlsx")
        print()
        sys.exit(1)
    
    excel_path = sys.argv[1]
    
    # Verificar que el archivo Excel existe
    if not os.path.exists(excel_path):
        print(f"❌ Error: No se encuentra el archivo: {excel_path}")
        sys.exit(1)
    
    # Buscar el archivo index.html
    html_path = "index.html"
    if not os.path.exists(html_path):
        print(f"❌ Error: No se encuentra index.html en el directorio actual")
        print(f"   Asegúrate de ejecutar este script en la misma carpeta que index.html")
        sys.exit(1)
    
    try:
        # Paso 1: Convertir Excel a JavaScript (y guardar histórico)
        js_data, num_bonds, historical_data = excel_to_js_data(excel_path)
        
        # Paso 2: Actualizar HTML
        if not update_html_file(html_path, js_data):
            sys.exit(1)
        
        # Paso 3: Actualizar fecha
        update_date_in_html(html_path)
        
        print()
        print("=" * 60)
        print("✅ ¡ACTUALIZACIÓN COMPLETADA!")
        print("=" * 60)
        print(f"📊 Total de bonos actualizados: {num_bonds}")
        if historical_data:
            print(f"💾 Snapshots históricos guardados: {len(historical_data['snapshots'])}")
        print()
        print("📄 PRÓXIMOS PASOS:")
        print("   1. Revisa el archivo index.html")
        print("   2. Sube los cambios a GitHub:")
        print()
        print("      git add index.html historical_data.json")
        print('      git commit -m "Actualizar datos de bonos"')
        print("      git push")
        print()
        print("   3. Vercel actualizará automáticamente en ~30 segundos")
        print()
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
