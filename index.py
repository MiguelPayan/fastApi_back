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

# Modelo Pydantic para la actualización del registro
class UpdateRecord(BaseModel):
    Nombre: str = None
    Edad: int = None
    Equipo: str = None
    Rendimiento: int = None
    Potencial: int = None
    valor_mercado: float = None

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
        global data 
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
        global data
        
        # Convertir el DataFrame a una lista de diccionarios
        players = data.to_dict(orient="records")
        
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un jugador
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
        global data 

        nuevo_registro = {
            "Nombre": record.Nombre,
            "Edad": record.Edad,
            "Equipo": record.Equipo,
            "Rendimiento": record.Rendimiento,
            "Potencial": record.Potencial,
            "Valor en el mercado": record.valor_mercado  
        }

        data = pd.DataFrame(data)
        nuevo_registro = pd.Series(nuevo_registro)
        nuevo_registro = pd.DataFrame(nuevo_registro,index=None)
        data = pd.concat([data,nuevo_registro.transpose()],ignore_index=True)

        data.to_csv('JugadoresMayorMenos.csv', index=False)
        data = pd.read_csv('JugadoresMayorMenos.csv')
        print(record)
        
        return {"message": "Jugador agregado exitosamente!"}
    except Exception as e:
        print(record)
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para modificar un jugador
@app.put("/jugadores/{nombre}")
async def actualizar_jugador(nombre: str, record: UpdateRecord):
    global data

    # Verificar si el registro existe
    if nombre not in data.Nombre.to_list():
        raise HTTPException(status_code=404, detail="Nombre no encontrado")

    # Obtener el índice del jugador a actualizar
    index = data[data["Nombre"] == nombre].index[0]

    # Actualizar los campos si se proporcionan
    if record.Nombre is not None:
        data.at[index, "Nombre"] = record.Nombre
    if record.Edad is not None:
        data.at[index, "Edad"] = record.Edad
    if record.Equipo is not None:
        data.at[index, "Equipo"] = record.Equipo
    if record.Rendimiento is not None:
        data.at[index, "Rendimiento"] = record.Rendimiento
    if record.Potencial is not None:
        data.at[index, "Potencial"] = record.Potencial
    if record.valor_mercado is not None:
        data.at[index, "Valor en el mercado"] = record.valor_mercado

    # Guardar el DataFrame actualizado en el archivo CSV
    data.to_csv('JugadoresMayorMenos.csv', index=False)

    return {"message": "Jugador actualizado correctamente", "user": record}
