import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

# Seguridad de FastAPI
security = HTTPBearer()

# Clave secreta
SECRET_KEY = 'secretkey'

# Generar token con expiración (opcional)
def createToken(data: dict, expires_in_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm='HS256')
    return token

# Validar token desde el encabezado
def validateToken(token: str):
    try:
        decoded_data = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido o no autorizado")

# Dependencia para proteger rutas
def jwt_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return validateToken(credentials.credentials)
