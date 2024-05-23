# Endpoint para agregar un nuevo registro al CSV
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
@app.delete("/jugadores/{nombre}", tags=["Jugadores"])
async def eliminar_jugador(nombre: str):
    try:
        data = pd.read_csv('JugadoresMayorMenos.csv')
        jugador_index = data[data['Nombre'] == nombre].index
        if len(jugador_index) == 0:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        data.drop(jugador_index, inplace=True)
        data.to_csv("JugadoresMayorMenos.csv", index=False)
        return {"mensaje": "Jugador eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
