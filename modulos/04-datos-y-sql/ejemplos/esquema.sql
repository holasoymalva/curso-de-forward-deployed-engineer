-- ==============================================================================
-- esquema.sql
-- Definición DDL para la base de datos relacional de Distribuidora Halcón.
-- Compatible con SQLite 3 y adaptable a PostgreSQL / MySQL.
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Tabla de Almacenes
CREATE TABLE IF NOT EXISTS almacenes (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    estado TEXT NOT NULL
);

-- 2. Tabla de Catálogo Maestro de Productos
CREATE TABLE IF NOT EXISTS productos (
    sku TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio > 0),
    stock_minimo INTEGER NOT NULL DEFAULT 20 CHECK(stock_minimo >= 0)
);

-- 3. Tabla de Inventario de Existencias Físicas
CREATE TABLE IF NOT EXISTS inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    almacen_codigo TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
    fecha_actualizacion TEXT NOT NULL,
    FOREIGN KEY (sku) REFERENCES productos(sku) ON DELETE CASCADE,
    FOREIGN KEY (almacen_codigo) REFERENCES almacenes(codigo) ON DELETE CASCADE,
    UNIQUE(sku, almacen_codigo)
);

-- 4. Tabla de Tiendas Clientes
CREATE TABLE IF NOT EXISTS tiendas (
    id_tienda TEXT PRIMARY KEY,
    nombre_tienda TEXT NOT NULL,
    contacto TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    ciudad TEXT NOT NULL,
    estado TEXT NOT NULL
);

-- 5. Tabla de Pedidos Cabecera
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY,
    tienda_id TEXT NOT NULL,
    almacen_codigo TEXT NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('pendiente', 'surtido', 'enviado', 'entregado', 'cancelado')),
    fecha TEXT NOT NULL,
    FOREIGN KEY (tienda_id) REFERENCES tiendas(id_tienda),
    FOREIGN KEY (almacen_codigo) REFERENCES almacenes(codigo)
);

-- 6. Tabla de Líneas de Pedido
CREATE TABLE IF NOT EXISTS lineas_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    sku TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (sku) REFERENCES productos(sku)
);

-- Índices para acelerar búsquedas comunes
CREATE INDEX IF NOT EXISTS idx_inventario_almacen ON inventario(almacen_codigo);
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria);
CREATE INDEX IF NOT EXISTS idx_pedidos_estado ON pedidos(estado);
