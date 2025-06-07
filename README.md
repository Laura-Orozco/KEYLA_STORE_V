# 🛍️ Keyla's Store - API Backend

Bienvenid@ a la API de **Keyla's Store**, una tienda de ropa construida como proyecto académico. Esta API permite gestionar usuarios, clientes, productos, categorías, proveedores y ventas -  Laura Orozco - Kevin Arzuza .

---

## 🔗 URL base de la API

```
http://localhost:8000
```

---

## 📄 Documentación interactiva

FastAPI genera automáticamente documentación para tu API:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🚀 Endpoints disponibles

### 👤 Usuarios

- `GET /usuarios/` → Obtener lista de usuarios
- `POST /usuarios/` → Crear nuevo usuario
- `GET /usuarios/{id_usuario}` → Obtener usuario por ID
- `PUT /usuarios/{id_usuario}` → Actualizar usuario
- `DELETE /usuarios/{id_usuario}` → Eliminar usuario

### 🧍 Clientes

- `GET /clientes/` → Obtener lista de clientes
- `POST /clientes/` → Crear cliente
- `GET /clientes/{cliente_id}` → Obtener cliente por ID
- `PUT /clientes/{id_cliente}` → Actualizar cliente

### 🗂️ Categorías

- `GET /categorias/` → Listar categorías
- `POST /categorias/` → Crear nueva categoría

### 🏢 Proveedores

- `GET /proveedores/` → Listar proveedores
- `POST /proveedores/` → Crear proveedor

### 🛒 Productos

- `GET /productos/` → Obtener lista de productos
- `POST /productos/` → Crear producto

### 💰 Ventas

- `POST /ventas/` → Crear una venta

---

## 🧬 Esquemas usados (Schemas)

- **CategoriaProducto**
  - `CategoriaProductoCreate`
  - `CategoriaProductoResponse`
- **Cliente**
  - `ClienteBase`
  - `ClienteCreate`
- **Producto**
  - `ProductoBase`
  - `ProductoCreate`
- **Proveedor**
  - `ProveedorBase`
  - `ProveedorCreate`
- **Usuario**
  - `UsuarioCreate`
  - `UsuarioResponse`
  - `UsuarioUpdate`
- **Venta**
  - `Venta`
  - `VentaCreate`
- **Errores**
  - `ValidationError`
  - `HTTPValidationError`

---

## 🧪 Tecnologías usadas

- **FastAPI** (backend)
- **MySQL** (base de datos, gestionada con HeidiSQL)
- **SQLAlchemy** (ORM)
- **Swagger / Redoc / Markdown** (documentación)
- **Bootstrap** (frontend - plantilla de Creative Tim)

---

## 🛠️ Cómo ejecutar el proyecto

```bash
# Activar el entorno virtual
env\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn app.main:app --reload
```

---

## 👩‍💻 Desarrolladores

- **Nombres:** Laura Orozco - Kevin Arzuza

