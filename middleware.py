from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

# Middleware personalizado con validación de token para el sistema de películas
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        # Usar el esquema HTTPBearer para extraer el token del encabezado
        auth = await super().__call__(request)

        # Validar el token con la función de genToken.py
        data = validateToken(auth.credentials)

        # Verificar que el token tenga una estructura válida
        if not isinstance(data, dict):
            raise HTTPException(status_code=401, detail="Token inválido")

        # Puedes ajustar esta parte para validar diferentes correos o roles
        # Por ejemplo, permitir más de un usuario autorizado:
        usuarios_autorizados = ["diana@example.com", "admin@peliculas.com"]
        if data.get('email') not in usuarios_autorizados:
            raise HTTPException(status_code=403, detail="Credenciales no válidas")

        # Si pasa todas las validaciones, se retorna la información del token
        return data
