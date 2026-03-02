# Configuración: Importación de librerías
# =============================================================================
# 1. Configuración: Importación de librerías
# =============================================================================
# En un notebook, esta sería la primera celda.
# Importamos las librerías necesarias para el análisis.
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
try:
    import seaborn as sns # Seaborn para visualizaciones más atractivas
except ImportError:
    sns = None
    print("Aviso: Seaborn no está instalado. Se usarán gráficos básicos de Matplotlib.")

# =============================================================================
# 2. Extracción (ETL): Carga y preparación de datos
# =============================================================================
# Esta sección se encargaría de obtener los datos. En un caso real,
# nos conectaríamos a una base de datos, una API, o leeríamos un archivo (CSV, Excel, etc.).
# Para este ejemplo, creamos los datos y simulamos un proceso ETL.

# Datos de origen
datos_origen = {
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
    'Ventas': [15000, 18500, 12000, 13500, 11000]
}
df_origen = pd.DataFrame(datos_origen)

# Simulación de ETL: Cargar a una base de datos y luego extraer para el análisis.
# Usamos un bloque try/finally para asegurar que la conexión se cierre siempre.
conn = None # Inicializamos por si falla la conexión
try:
    # Conexión a base de datos en memoria
    conn = sqlite3.connect(':memory:')
    # Carga de datos a la DB (la parte 'L' de ETL)
    df_origen.to_sql('ventas', conn, index=False, if_exists='replace')

    # Extracción de los datos para el análisis (la parte 'E' de ETL para nuestro script)
    # Añadimos un ORDER BY para que los datos ya vengan con una ordenación útil.
    query = "SELECT * FROM ventas ORDER BY Ventas DESC"
    df = pd.read_sql(query, conn)

except sqlite3.Error as e:
    print(f"Error en la base de datos: {e}")
    # Si hay un error, creamos un DataFrame vacío para que el script no falle.
    df = pd.DataFrame()
finally:
    if conn:
        conn.close()

# =============================================================================
# 3. Análisis: Exploración y procesamiento
# =============================================================================
# En esta fase, exploramos los datos, realizamos cálculos y transformaciones.

# Mostramos una vista previa de los datos
print("Datos de ventas por ciudad (ordenados de mayor a menor):")
print(df)
print("-" * 30)

# Realizamos el análisis principal: encontrar la ciudad con más ventas.
# Como los datos ya están ordenados, la primera fila es la de mayor venta.
if not df.empty:
    ciudad_max_ventas = df.iloc[0]
else:
    ciudad_max_ventas = None

# =============================================================================
# 4. Conclusiones y Visualización
# =============================================================================
# Aquí presentamos los hallazgos del análisis de forma clara, tanto textual
# como visualmente.

# Conclusión textual
if ciudad_max_ventas is not None:
    print(f"La ciudad con la venta más alta es {ciudad_max_ventas['Ciudad']} "
          f"con un total de {ciudad_max_ventas['Ventas']:,.0f} €.")
else:
    print("No se pudieron analizar los datos de ventas.")
print("-" * 30)

# Visualización de resultados
if not df.empty:
    print("Generando gráfico de ventas por ciudad...")
    if sns:
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Ciudad', y='Ventas', data=df, ax=ax, palette='viridis', hue='Ciudad', legend=False)
        ax.set_title('Ventas por Ciudad', fontsize=16, fontweight='bold')
        ax.set_xlabel('Ciudad', fontsize=12)
        ax.set_ylabel('Ventas (€)', fontsize=12)
        ax.tick_params(axis='x', rotation=0)
        ax.bar_label(ax.containers[0], fmt='{:,.0f} €')
        fig.text(0.99, 0.01, 'Generado con Seaborn', ha='right', fontsize=10, style='italic')
        plt.tight_layout()
    else:
        plt.figure(figsize=(10, 6))
        plt.bar(df['Ciudad'], df['Ventas'])
        plt.title('Ventas por Ciudad')
        plt.xlabel('Ciudad')
        plt.ylabel('Ventas (€)')
        plt.figtext(0.99, 0.01, 'Generado con Matplotlib', ha='right', fontsize=10, style='italic')
    plt.show()