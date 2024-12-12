import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ruta del archivo CSV
csv_file = "data.csv"

# Cargar los datos
# Se espera que el archivo tenga una columna 'Close' y 'Date'
data = pd.read_csv(csv_file)
data['Date'] = pd.to_datetime(data['Date'])  # Asegurarse de que 'Date' sea tipo datetime
data.set_index('Date', inplace=True)  # Establecer 'Date' como índice para análisis temporal

# Parámetros de Bollinger Bands
window = 20  # Tamaño de la ventana para el promedio móvil
num_std_dev = 2  # Multiplicador de la desviación estándar

# Cálculo de Bollinger Bands
data['SMA'] = data['Close'].rolling(window=window).mean()  # Promedio móvil simple
data['STD'] = data['Close'].rolling(window=window).std()  # Desviación estándar
data['Upper Band'] = data['SMA'] + (num_std_dev * data['STD'])  # Banda superior
data['Lower Band'] = data['SMA'] - (num_std_dev * data['STD'])  # Banda inferior

# Identificación de soporte y resistencia
# Soporte: Close toca o cruza la Banda Inferior
# Resistencia: Close toca o cruza la Banda Superior
data['Support'] = np.where(data['Close'] <= data['Lower Band'], True, False)
data['Resistance'] = np.where(data['Close'] >= data['Upper Band'], True, False)

# Guardar los resultados en un archivo CSV
output_file = "bollinger_bands_output.csv"
data.to_csv(output_file)

# Graficar las Bollinger Bands
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.plot(data.index, data['SMA'], label='SMA', color='orange')
plt.plot(data.index, data['Upper Band'], label='Upper Band', color='green', linestyle='--')
plt.plot(data.index, data['Lower Band'], label='Lower Band', color='red', linestyle='--')
plt.fill_between(data.index, data['Upper Band'], data['Lower Band'], color='gray', alpha=0.1)
plt.title('Bollinger Bands')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid()

# Guardar el gráfico como archivo
output_image = "bollinger_bands_plot.png"
plt.savefig(output_image)
plt.show()

print(f"Cálculo de Bollinger Bands completado. Resultados guardados en: {output_file}")
print(f"Gráfico guardado como: {output_image}")
