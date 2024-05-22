import pandas as pd

nombre_archivo = 'JugadoresMayorMenos.csv'

dataframe = pd.read_csv(nombre_archivo)

dataframe['Valor en el mercado'] = dataframe['Valor en el mercado'].str.replace('M', '')
# Quitar los renglones con la letra K en la columna de Valor en el mercado
dataframe = dataframe[~dataframe['Valor en el mercado'].str.contains('K')]
# Reemplazar "€" por una cadena vacía '' y luego convertir a tipo float
dataframe['Valor en el mercado'] = dataframe['Valor en el mercado'].str.replace('€', '').astype(float)

dataframe.to_csv("JugadoresMayorMenos.csv", index=False)

print(" \nDESPUES :D")
