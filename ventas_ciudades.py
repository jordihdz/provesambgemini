# Configuración: Importación de librerías
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Extracción (ETL): Conexión a la base de datos y carga de datos
datos = {
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
    'Ventas': [15000, 18500, 12000, 13500, 11000]
}

# Crear conexión a base de datos en memoria y cargar datos
conn = sqlite3.connect(':memory:')
pd.DataFrame(datos).to_sql('ventas', conn, index=False, if_exists='replace')

# Análisis: Consultas SQL y creación de DataFrames
df = pd.read_sql("SELECT * FROM ventas", conn)

# Conclusiones: Resultados visuales o tablas finales
print("Datos de ventas por ciudad:")
print(df)
print("-" * 30)

fila_maxima = df.loc[df['Ventas'].idxmax()]

print(f"La ciudad con la venta más alta es {fila_maxima['Ciudad']} "
      f"con un total de {fila_maxima['Ventas']} ventas.")

# Visualización
plt.bar(df['Ciudad'], df['Ventas'])
plt.title('Ventas por Ciudad')
plt.xlabel('Ciudad')
plt.ylabel('Ventas')
plt.show()

conn.close()