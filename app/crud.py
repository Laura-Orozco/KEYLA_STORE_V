
from sqlalchemy.orm import Session,joinedload
from . import models, schemas
from .models import Usuario
from .models import Cliente

from datetime import datetime

# --------- CATEGORIA PRODUCTO ---------
def create_categoria(db: Session, categoria: schemas.CategoriaProductoCreate):
    db_categoria = models.CategoriaProducto(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categorias(db: Session):
    return db.query(models.CategoriaProducto).all()
# --------- USUARIOS ---------
def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuarios(db: Session):
    return db.query(models.Usuario).all()

def get_usuario_by_id(db: Session, id_usuario: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

def obtener_usuario(db: Session):
    return db.query(models.Usuario).all()

def update_usuario(db: Session, usuario_id: int, usuario_data):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        for key, value in usuario_data.dict().items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario


# --------- PRODUCTOS ---------
def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def get_productos(db: Session):
    return db.query(models.Producto).options(
        joinedload(models.Producto.proveedor),
        joinedload(models.Producto.categoria)
    ).all()



def obtener_productos(db: Session):
    return db.query(models.Producto).all()

def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return True
    return False



def get_proveedores(db: Session):         
       #intento llamar categoria
    return db.query(models.CategoriaProducto).all()





# --------- PROVEEDORES ---------
def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    db_proveedor = models.Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def get_proveedores(db: Session):

    return db.query(models.Proveedor).options(joinedload(models.Proveedor.categoria)).all()

def obtener_proveedores(db: Session):
    return db.query(models.Proveedor).all()

def get_categorias(db: Session):         
       #intento llamar categoria
    return db.query(models.CategoriaProducto).all()


def eliminar_proveedor(db: Session, proveedor_id: int):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == proveedor_id).first()
    if proveedor:
        db.delete(proveedor)
        db.commit()
        return True
    return False

def editar_proveedor(db: Session, proveedor_id: int, datos_actualizados: schemas.ProveedorUpdate):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == proveedor_id).first()
    if not proveedor:
        return None
    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(proveedor, key, value)
    db.commit()
    db.refresh(proveedor)
    return proveedor



# --------- VENTAS ---------

def crear_venta(db: Session, venta: schemas.VentaCreate):
    db_venta = models.Venta(**venta.dict())

    if not db_venta.fecha_venta:
        db_venta.fecha_venta = datetime.now()

    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta

# --------- CLIENTES ---------


def crear_cliente(db: Session, cliente: schemas.ClienteCreate):
    nuevo_cliente = models.Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

def get_clientes(db: Session):
    return db.query(models.Cliente).all()


def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
        return True
    return False