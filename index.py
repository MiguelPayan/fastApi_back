from fastapi import FastAPI, HTTPException
from fastapi import Request
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
        global data 

        #data = pd.DataFrame(data)

        nuevo_registro = {
            "Nombre": record.Nombre,
            "Edad": record.Edad,
            "Equipo": record.Equipo,
            "Rendimiento": record.Rendimiento,
            "Potencial": record.Potencial,
            "Valor en el mercado": record.valor_mercado  
        }

        data.loc[len(data)] = nuevo_registro
        data.to_csv('JugadoresMayorMenos.csv', index=False)
        print(record)
        
        
        return {"message": "Jugador agregado exitosamente!"}
    except Exception as e:
        print(record)
        raise HTTPException(status_code=500, detail=str(e))