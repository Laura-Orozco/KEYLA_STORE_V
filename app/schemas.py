from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime

# --------- USUARIO ---------
class UsuarioBase(BaseModel):
    nombre_usuario: str
    usuario: str
    contraseña_usuario: str
    correo_usuario: str

class UsuarioCreate(UsuarioBase):
    contraseña_usuario: str 

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True  

class UsuarioUpdate(BaseModel):
    nombre_usuario: str
    usuario: str
    correo_usuario: str
    contraseña_usuario: Optional[str] = None  

class Usuario(UsuarioBase):
    id_usuario: int

# --------- CATEGORIA PRODUCTO ---------
class CategoriaProducto(BaseModel):
    nombre_categoria: str
    descripcion_categoria: Optional[str] = None

class CategoriaProductoCreate(CategoriaProducto):
    pass

class CategoriaProductoResponse(CategoriaProducto):
    id_categoria: int

    class Config:
        from_attributes = True

# --------- CLIENTE ---------

class ClienteBase(BaseModel):
    nombre_cliente: str
    identificacion: str
    correo_cliente: str
    telefono_cliente: str
    direccion_cliente: str

    class Config:
        orm_mode = True

class ClienteCreate(ClienteBase):
    pass

class clienteResponse(BaseModel):
    id_cliente: int
    nombre_cliente: str
    identificacion: str
    correo_cliente: str
    telefono_cliente: str
    direccion_cliente: str

# --------- PROVEEDOR ---------
class ProveedorBase(BaseModel):
    nombre_proveedor: str
    telefono_proveedor: Optional[str] = None
    correo_proveedor: Optional[str] = None
    id_categoria: int

class ProveedorCreate(ProveedorBase):
    pass
class CategoriaBase(BaseModel):
    id_categoria: int
    nombre_categoria: str

    class Config:
        orm_mode = True
class ProveedorResponse(BaseModel):
    id_proveedor: int
    nombre_proveedor: str
    telefono_proveedor: Optional[str]
    correo_proveedor: Optional[str]
    id_categoria: int
    categoria: Optional[CategoriaBase]  # Esto es clave

    class Config:
        from_attributes = True


class CategoriaResponse(BaseModel):  #intento relacionar categoria
    id_categoria: int
    nombre_categoria: str

    class Config:
        from_attributes = True

class ProveedorUpdate(BaseModel):
    nombre_proveedor: str
    telefono_proveedor: str
    correo_proveedor: str
    id_categoria: int




# --------- PRODUCTO ---------
class ProductoBase(BaseModel):
    nombre_producto: str
    descripcion_producto: Optional[str] = None
    stock_producto: int
    precio_producto: float
    id_categoria: int
    id_proveedor: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(BaseModel):
    id_producto: int
    categoria: Optional[CategoriaBase]
    proveedor: Optional[ProveedorBase]


    class Config:
        from_attributes = True


#-------------- VENTAS -----------------
class VentaCreate(BaseModel):
    id_producto: int
    id_cliente: int
    id_usuario: int
    precio: float

    
class Venta(VentaCreate):
    id_venta: int

    class Config:
        orm_mode = True