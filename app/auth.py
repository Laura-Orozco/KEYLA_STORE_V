from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import JWTError, jwt  # <-- Agregado

from .models import Usuario
from .database import SessionLocal

# JWT config
SECRET_KEY = "clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Verificación simple (usa bcrypt en producción)
def verify_password(plain_password, stored_password):
    return plain_password == stored_password

# Autenticación
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Usuario).filter(Usuario.usuario == username).first()
    if not user:
        return None
    if not verify_password(password, user.contraseña_usuario):
        return None
    return user


# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Obtener usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.usuario == username).first()
    if user is None:
        raise credentials_exception
    return user

# Esta función extra si la necesitas importar como `verify_token`
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
