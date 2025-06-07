
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
#from .auth import create_access_token, verify_token
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    Token,
    get_db,verify_token
)
from app.schemas import UsuarioUpdate  
from app.models import Usuario
from . import models, schemas, crud
from .database import SessionLocal, engine
from typing import List  # ¡Importación necesaria!


#inicial
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/login/")
def read_root():
    return JSONResponse(content={"message": "Bienvenido", "status": "active"})



# --- RUTAS--------

@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate):
    db = SessionLocal()
    # Aquí iría tu lógica para crear el usuario
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    db.close()
    return db_usuario

@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios():
    db = SessionLocal()
    usuarios = db.query(models.Usuario).all()
    db.close()
    return usuarios

@app.get("/usuarios/")
def get_usuarios(db: Session = Depends(get_db), ):
    return crud.obtener_usuario(db)

@app.put("/usuarios/{id_usuario}")
def actualizar_usuario(id_usuario: int, datos_actualizados: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        usuario_db = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar los campos
        usuario_db.nombre_usuario = datos_actualizados.nombre_usuario
        usuario_db.usuario = datos_actualizados.usuario
        usuario_db.correo_usuario = datos_actualizados.correo_usuario
        
        if datos_actualizados.contraseña_usuario:
            usuario_db.contraseña_usuario = datos_actualizados.contraseña_usuario

        db.commit()
        db.refresh(usuario_db)
        return {"mensaje": "Usuario actualizado con éxito", "usuario": usuario_db}
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: " + str(e.orig))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")

@app.get("/usuarios/{id_usuario}")
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario de la base de datos
    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado con éxito"}

# Categorias ---------------------------------------------------------------
@app.post("/categorias/", response_model=schemas.CategoriaProductoResponse)
def crear_categoria(categoria: schemas.CategoriaProductoCreate, db: Session = Depends(get_db)):
    db_categoria = models.CategoriaProducto(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria



# Clientes ---------------------------------------------------------------------------------
@app.post("/clientes/", response_model=schemas.ClienteBase)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.crear_cliente(db=db, cliente=cliente)

# Obtener todos los clientes
@app.get("/clientes/", response_model=list[schemas.clienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.get_clientes(db=db)



@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    resultado = crud.eliminar_cliente(db, cliente_id)
    if resultado:
        return {"mensaje": "cliente eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="cliente no encontrado")


@app.get("/usuarios/{id_usuario}")
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario de la base de datos
    db.delete(usuario)
    db.commit()


# Proveedores-----------------------------------------------------------------------------------
@app.post("/proveedores/", response_model=schemas.ProveedorBase)
def crear_proveedor(proveedor: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    return crud.create_proveedor(db=db, proveedor=proveedor)

@app.get("/proveedores/", response_model=list[schemas.ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db)):
    return crud.get_proveedores(db=db)

@app.delete("/proveedores/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    resultado = crud.eliminar_proveedor(db, proveedor_id)
    if resultado:
        return {"mensaje": "Proveedor eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")

@app.get("/proveedores/{proveedor_id}")
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@app.put("/proveedores/{proveedor_id}")
def actualizar_proveedor(proveedor_id: int, proveedor_actualizado: schemas.ProveedorUpdate, db: Session = Depends(get_db)):
    proveedor_db = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == proveedor_id).first()
    if not proveedor_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    proveedor_db.nombre_proveedor = proveedor_actualizado.nombre_proveedor
    proveedor_db.telefono_proveedor = proveedor_actualizado.telefono_proveedor
    proveedor_db.correo_proveedor = proveedor_actualizado.correo_proveedor
    proveedor_db.id_categoria = proveedor_actualizado.id_categoria  # si usas categorías

    db.commit()
    db.refresh(proveedor_db)
    return proveedor_db



# Productos ---------------------------------------------------------------------------------
@app.post("/productos/", response_model=schemas.ProductoBase)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

@app.get("/productos/", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.get_productos(db=db)

@app.get("/productos/")
def get_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    resultado = crud.eliminar_producto(db, producto_id)
    if resultado:
        return {"mensaje": "producto eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="producto no encontrado")

@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])  #intento listar categorias
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)


# Ventas-----------------------------------------------------------------------------------


@app.post("/ventas/", response_model=schemas.Venta)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    return crud.crear_venta(db=db, venta=venta)

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    access_token = create_access_token(
        data={"sub": user.nombre_usuario}  # Aquí usas el campo correcto
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {
        "username": current_user.username,
        "full_name": current_user.full_name
    }
