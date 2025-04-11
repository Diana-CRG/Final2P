from pydantic import BaseModel, Field, EmailStr

# Modelo de autenticación (para login o generación de token)
class ModeloAuth(BaseModel):
    email: EmailStr = Field(..., description="Correo válido", example="correo@gmail.com")
    passw: str = Field(..., min_length=8, description="Contraseña con mínimo 8 caracteres")

# Modelo de validación para películas
class ModeloPelicula(BaseModel):
    Titulo: str = Field(..., min_length=2, description="Título de la película")
    Genero: str = Field(..., min_length=4, description="Género de la película")
    Año: int = Field(..., ge=1000, le=9999, description="Año de estreno")
    Clasificacion: str = Field(..., min_length=1, max_length=5, description="Clasificación de la película")
