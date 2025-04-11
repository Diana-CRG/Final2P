from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from genToken import jwt_required
from modelsPydantic import ModeloPelicula
from genToken import createToken
from fastapi import Body




app= FastAPI(
    title='Examen Segundo Parcial',
    description='Diana Carolina Ruiz García',
    version='1.0.1'
)



peliculas = [
    {"id": 1,"Titulo": "El Señor de los Anillos: La Comunidad del Anillo", "Genero": "Fantasía", "Año": 2001, "Clasificacion": "PG-13"},
    {"id": 2,"Titulo": "Interestelar", "Genero": "Ciencia Ficción", "Año": 2014, "Clasificacion": "PG-13"},
    {"id": 3,"Titulo": "Titanic", "Genero": "Romance/Drama", "Año": 1997, "Clasificacion": "PG-13"},
    {"id": 4,"Titulo": "El Rey León", "Genero": "Animación", "Año": 1994, "Clasificacion": "G"},
    {"id": 5,"Titulo": "John Wick", "Genero": "Acción", "Año": 2014, "Clasificacion": "R"}
]


#Endpoint home

@app.get('/', tags=['Hola Mundo'])
def home():
    return{'Hello':'World FastAPI'}


 #Consultar todas las películas
@app.get("/peliculas", tags=["Consultar todas"])
def obtener_todas():
    return {"Películas registradas": peliculas}

# Consultar una sola película
@app.get("/pelicula/{id}", tags=["Consultar una"])
def obtener_una(id: int):
    for peli in peliculas:
        if peli["id"] == id:
            return peli
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Agregar nueva película
@app.post("/pelicula", tags=["Añadir"])
def agregar_pelicula(pelicula: ModeloPelicula):
    nueva = pelicula.dict()
    nueva["id"] = len(peliculas) + 1
    peliculas.append(nueva)
    return nueva

#  Editar película existente
@app.put("/pelicula/{id}", tags=["Editar"])
def editar_pelicula(id: int, datos: ModeloPelicula):
    for index, peli in enumerate(peliculas):
        if peli["id"] == id:
            peliculas[index].update(datos.dict())
            return peliculas[index]
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Eliminar película (protegido con JWT)@app.delete("/pelicula/{id}", tags=["Eliminar Película (protegido con JWT)"])
@app.delete("/pelicula/{id}", tags=["Eliminar Película (protegido con JWT)"])
def eliminar_pelicula(id: int, token_data: dict = Depends(jwt_required)):
    for index, peli in enumerate(peliculas):
        if peli["id"] == id:
            peliculas.pop(index)
            return {"msg": "Película eliminada"}
    raise HTTPException(status_code=404, detail="Película no encontrada")





#TOKEN

@app.post("/login", tags=["Autenticación"])
def login(email: str = Body(..., embed=True)):
    usuarios_autorizados = ["diana@example.com", "admin@peliculas.com"]
    if email not in usuarios_autorizados:
        raise HTTPException(status_code=403, detail="Correo no autorizado")

    token = createToken({"email": email})
    return {"access_token": token}
