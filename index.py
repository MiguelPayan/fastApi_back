from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

# Modelo Pydantic para validar el nuevo registro
class NewRecord(BaseModel):
    Nombre: str
    Edad: int
    Equipo: str
    Rendimiento: int
    Potencial: int
    valor_mercado: float  

# Inicializar la aplicación FastAPI
app = FastAPI()

data = pd.read_csv('JugadoresMayorMenos.csv')

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes, puedes restringirlo a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)
# Endpoint para reestablecer el df
@app.get("/reestablecer")
def reestablecer():
    try:
        # Leer el archivo CSV modificado
        data = pd.read_csv('JugadoresMayorMenosORIGINAL.csv')

        data.to_csv('JugadoresMayorMenos.csv', index=False)

        return {"message": "Dataframe Reestablecido Correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los jugadores
@app.get("/jugadores")
def read_data():
    try:
        # Leer el archivo CSV
        data = pd.read_csv('JugadoresMayorMenos.csv')
        
        # Convertir el DataFrame a una lista de diccionarios
        data = data.to_dict(orient="records")
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para eliminar un jugador
@app.delete("/jugadores/{nombre}")
def delete_item(nombre: str):
    global data
    # Verificar si el registro existe
    if nombre not in data.Nombre.to_list():
        print("Nombre no encontrado")
        print(data.Nombre.to_list())
        raise HTTPException(status_code=404, detail="Nombre no encontrado")
    else:
        # Eliminar el registro
        print("si entra")
        print(nombre)
        data = data[data["Nombre"] != nombre]
        # Guardar el DataFrame actualizado en el archivo CSV
        data.to_csv('JugadoresMayorMenos.csv', index=False)
    
        return {"message": nombre + " eliminado exitosamente :D"}
    
    
    
    

# Ruta para agregar un nuevo registro al CSV
@app.post("/jugadores/")
def add_record(record: NewRecord):
    try:
        data = pd.read_csv('JugadoresMayorMenos.csv')
        
        # Convertir el nuevo registro a un DataFrame
        new_data = pd.DataFrame([record.dict()])
        
        # Concatenar el DataFrame existente con el nuevo registro
        data = pd.concat([data, new_data], ignore_index=True)
        
        # Guardar el DataFrame actualizado de nuevo en el archivo CSV
        data.to_csv("JugadoresMayorMenos.csv", index=False)
        
        return {"message": "Jugador agregado exitosamente!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener información sobre un jugador específico por nombre
@app.get("/jugadores/{nombre}", tags=["Jugadores"])
async def get_jugador(nombre: str):
    try:
        data = pd.read_csv('JugadoresMayorMenos.csv')
        jugador = data[data['Nombre'] == nombre]
        if jugador.empty:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return jugador.to_dict(orient="records")[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar la información de un jugador
@app.put("/jugadores/{nombre}", tags=["Jugadores"])
async def actualizar_jugador(nombre: str, edad: int, equipo: str, rendimiento: float, potencial: float, valor_mercado: float):
    try:
        data = pd.read_csv('JugadoresMayorMenos.csv')
        jugador_index = data[data['Nombre'] == nombre].index
        if len(jugador_index) == 0:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        data.loc[jugador_index, ['Edad', 'Equipo', 'Rendimiento', 'Potencial', 'Valor en el mercado']] = [edad, equipo, rendimiento, potencial, valor_mercado]
        data.to_csv("JugadoresMayorMenos.csv", index=False)
        return {"mensaje": "Información del jugador actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un jugador
# @app.delete("/jugadores/{nombre}", tags=["Jugadores"])
# async def eliminar_jugador(nombre: str):
#     jugador_index = data[data['Nombre'] == nombre].index
#     if len(jugador_index) == 0:
#         raise HTTPException(status_code=404, detail="Jugador no encontrado")
#     data.drop(jugador_index, inplace=True)
#     return {"mensaje": "Jugador eliminado correctamente"}

# Endpoint para obtener jugadores por equipo
@app.get("/equipos/{equipo}", tags=["Equipos"])
async def get_jugadores_por_equipo(equipo: str):
    jugadores = data[data['Equipo'] == equipo]
    if jugadores.empty:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return jugadores.to_dict(orient="records")

# Endpoint para obtener jugadores por rango de edad
@app.get("/jugadores/edad/", tags=["Jugadores"])
async def get_jugadores_por_edad(edad_min: int, edad_max: int):
    jugadores = data[(data['Edad'] >= edad_min) & (data['Edad'] <= edad_max)]
    if jugadores.empty:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores en el rango de edad especificado")
    return jugadores.to_dict(orient="records")
