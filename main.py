# crear un gráfico de barras con las ventas de 3 frutas usando matplotlib
import matplotlib.pyplot as plt

# Datos de ventas
frutas = ['Manzanas', 'Plátanos', 'Naranjas']
ventas = [50, 30, 20]

# Crear el gráfico de barras
plt.bar(frutas, ventas)
plt.xlabel('Frutas')
plt.ylabel('Ventas')
plt.title('Ventas de Frutas')
plt.show()