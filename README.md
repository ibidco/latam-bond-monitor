# 📊 Monitor de Bonos LATAM - Guía de Actualización

Esta guía te muestra cómo actualizar los datos del monitor de bonos con **seguimiento histórico de precios**.

## 🆕 Nuevas Funcionalidades

✅ **Histórico de precios**: Guarda snapshots cada vez que actualizas  
✅ **Cambios visuales**: Muestra cambios de precio en 1 semana, 1 mes y 3 meses  
✅ **Colores intuitivos**: Verde para subidas, rojo para bajadas  
✅ **Exportación completa**: Incluye cambios históricos en el Excel descargado  

---

## 📋 Requisitos

1. **Python 3.7 o superior** instalado en tu computadora
2. **Git** instalado
3. Tu repositorio clonado localmente

---

## 🔧 Instalación Inicial (Solo una vez)

### Paso 1: Instalar Python
Si no tienes Python instalado:
- **Windows**: Descarga desde https://www.python.org/downloads/
- **Mac**: Viene preinstalado, o usa `brew install python3`
- **Linux**: Usa `sudo apt install python3 python3-pip`

### Paso 2: Instalar Dependencias
Abre una terminal/CMD en la carpeta de tu proyecto y ejecuta:

```bash
pip install pandas openpyxl
```

### Paso 3: Clonar tu Repositorio (si aún no lo has hecho)

```bash
git clone https://github.com/TU-USUARIO/latam-bond-monitor.git
cd latam-bond-monitor
```

---

## 🚀 Actualizar Datos (Cada vez que tengas nuevo Excel)

### Método 1: Script Automático (Recomendado)

**Windows:**
1. Guarda tu nuevo Excel en la carpeta del repositorio como `Monitor_de_spreads.xlsx`
2. **Doble clic** en `actualizar.bat`
3. ¡Listo! Todo se hace automáticamente

**Mac/Linux:**
1. Guarda tu nuevo Excel en la carpeta como `Monitor_de_spreads.xlsx`
2. Ejecuta en terminal: `./actualizar.sh`
3. ¡Listo!

### Método 2: Paso a Paso Manual

1. **Guarda tu nuevo Excel** en la carpeta del repositorio como `Monitor_de_spreads.xlsx`

2. **Ejecuta el script**:
   ```bash
   python update_bond_data.py Monitor_de_spreads.xlsx
   ```

3. **Verás algo como esto**:
   ```
   ============================================================
   🚀 ACTUALIZADOR DE DATOS - MONITOR DE BONOS LATAM
      Con seguimiento histórico de precios
   ============================================================
   
   📖 Leyendo archivo Excel: Monitor_de_spreads.xlsx
   ✅ Encontrados 561 bonos
   💾 Guardando snapshot histórico...
   ✅ Snapshot guardado. Total snapshots: 5
   📊 Calculando cambios de precio...
   🔧 Actualizando archivo HTML: index.html
   ✅ Archivo HTML actualizado exitosamente
   📅 Actualizando fecha de corte...
   ✅ Fecha actualizada a: Mar 24, 2026
   
   ============================================================
   ✅ ¡ACTUALIZACIÓN COMPLETADA!
   ============================================================
   📊 Total de bonos actualizados: 561
   💾 Snapshots históricos guardados: 5
   ```

4. **Sube los cambios a GitHub**:
   ```bash
   git add index.html historical_data.json
   git commit -m "Actualizar datos de bonos con histórico"
   git push
   ```

5. **¡Listo!** Vercel detecta el cambio y actualiza tu sitio en ~30 segundos

---

## 📈 Cómo Funciona el Histórico

### Archivo de Histórico
- Se crea un archivo `historical_data.json` que guarda snapshots de precio, YTW y spread
- Cada vez que actualizas, se agrega un nuevo snapshot con la fecha
- Solo se guardan los últimos **90 días** para mantener el archivo pequeño

### Visualización en la Web
La tabla ahora muestra 3 columnas adicionales:
- **Δ 1W**: Cambio de precio vs. 1 semana atrás
- **Δ 1M**: Cambio de precio vs. 1 mes atrás  
- **Δ 3M**: Cambio de precio vs. 3 meses atrás

**Colores:**
- 🟢 **Verde**: El precio subió
- 🔴 **Rojo**: El precio bajó
- ⚪ **Gris**: Sin cambio o sin datos históricos

### Exportación
El botón "Download Excel" ahora incluye estas columnas de cambio histórico, respetando los filtros activos.

---

## 🔄 Flujo Completo de Actualización

```
Nuevo Excel → Ejecutar Script → Git Push → Vercel Actualiza Automáticamente
   (2 min)         (10 seg)        (10 seg)          (30 seg)

Total: ~3 minutos
```

---

## 📁 Estructura de Archivos

```
latam-bond-monitor/
├── index.html                  # Página web principal
├── Monitor_de_spreads.xlsx     # Tu archivo Excel (no se sube a web)
├── historical_data.json        # Histórico de precios (SE SUBE)
├── update_bond_data.py         # Script de actualización
├── actualizar.bat              # Script Windows automático
├── actualizar.sh               # Script Mac/Linux automático
└── README.md                   # Esta guía
```

**Importante**: El archivo `historical_data.json` debe subirse a GitHub junto con `index.html`

---

## 🔍 Comandos de Git (Referencia Rápida)

```bash
# Ver estado de cambios
git status

# Agregar cambios
git add index.html historical_data.json

# Hacer commit
git commit -m "Actualizar datos de bonos - Mar 2026"

# Subir a GitHub
git push

# Si hay conflictos, usar tu versión local
git pull origin main
git checkout --ours index.html
git add index.html
git commit -m "Resolver conflictos"
git push

# Ver historial
git log --oneline
```

---

## ⚠️ Solución de Problemas

### Error: "No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### Error: "git: command not found"
Instala Git desde: https://git-scm.com/downloads

### Error: "Permission denied (publickey)"
Configura tu SSH key en GitHub:
```bash
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
# Luego agrega la key en GitHub Settings → SSH Keys
```

### El sitio no muestra cambios históricos
- **Primera actualización**: No habrá datos históricos (es normal)
- **Segunda actualización**: Comenzarás a ver cambios vs. la primera vez
- **Tercera+ actualización**: Verás cambios en 1W, 1M, 3M según disponibilidad

### Conflictos en Git
Si hay conflictos al hacer `git pull`:
```bash
git pull origin main
git checkout --ours index.html
git checkout --ours historical_data.json
git add index.html historical_data.json
git commit -m "Resolver conflictos con versión local"
git push
```

---

## 💡 Consejos

- **Haz backup** de tu Excel antes de actualizar
- **Actualiza regularmente** (semanal o quincenal) para mejor histórico
- **Revisa los datos** en local antes de hacer push
- **Usa mensajes descriptivos** en los commits (ej: "Actualizar bonos - Q1 2026")
- **Primera semana**: No verás cambios históricos (es normal)
- **Después de 3 actualizaciones**: Tendrás datos completos de tendencia

---

## 📊 Ejemplo de Uso

**Semana 1 (Mar 10):**
- Actualizas por primera vez
- No hay cambios históricos (todo en blanco)
- Se guarda el primer snapshot

**Semana 2 (Mar 17):**
- Actualizas de nuevo
- Columna "Δ 1W" muestra cambios vs. Mar 10
- Las otras columnas aún vacías

**Mes 2 (Abr 10):**
- Actualizas mensualmente
- "Δ 1W", "Δ 1M" muestran datos
- "Δ 3M" todavía vacío

**Mes 4 (Jun 10):**
- ¡Todas las columnas tienen datos!
- Puedes ver tendencias completas

---

## 🎯 Resumen Rápido

1. **Guarda** tu Excel como `Monitor_de_spreads.xlsx`
2. **Doble clic** en `actualizar.bat` (Windows) o ejecuta `./actualizar.sh` (Mac/Linux)
3. **Espera** ~30 segundos para ver tu sitio actualizado
4. **¡Disfruta** del seguimiento histórico de precios!

---

**Última actualización: Marzo 2026**
