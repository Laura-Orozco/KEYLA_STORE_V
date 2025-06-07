
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from sqlalchemy import func

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String)
    usuario = Column(String)
    contraseña_usuario = Column(String)
    correo_usuario = Column(String)

class CategoriaProducto(Base):
    __tablename__ = "categoria_productos"

    id_categoria = Column(Integer, primary_key=True, index=True) 
    nombre_categoria = Column(String(100), nullable=False)
    descripcion_categoria = Column(Text)

    productos = relationship("Producto", back_populates="categoria")
    proveedores = relationship("Proveedor", back_populates="categoria")


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(100), nullable=False)
    identificacion = Column(String(20))
    correo_cliente = Column(String(100))
    telefono_cliente = Column(String(20))
    direccion_cliente = Column(Text)



class Proveedor(Base):
    __tablename__ = "proveedor"

    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre_proveedor = Column(String(100), nullable=False)
    telefono_proveedor = Column(String(20))
    correo_proveedor = Column(String(100))
    id_categoria = Column(Integer, ForeignKey("categoria_productos.id_categoria"))

    categoria = relationship("CategoriaProducto", back_populates="proveedores")
    productos = relationship("Producto", back_populates="proveedor")



class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre_producto = Column(String(100), nullable=False)
    descripcion_producto = Column(Text)
    stock_producto = Column(Integer, default=0)
    precio_producto = Column(DECIMAL(10,2), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categoria_productos.id_categoria')) 
    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor"))

    categoria = relationship("CategoriaProducto", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    ventas = relationship("Venta", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    fecha_venta = Column(DateTime(timezone=True), server_default=func.now())

    producto = relationship("Producto", back_populates="ventas")



    
