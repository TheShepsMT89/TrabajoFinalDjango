# API de Facturación

Este proyecto proporciona una API para gestionar facturas de clientes y proveedores, incluyendo funcionalidades para exportar e importar datos en formatos Excel y PDF.

## Endpoints

### Exportar Datos

#### Exportar Datos a Excel

- **URL:** `/api/auth/exportar-datos-excel/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Descripción:** Exporta todas las facturas de clientes o proveedores a un archivo Excel.

#### Exportar Datos a PDF

- **URL:** `/api/auth/exportar-datos-pdf/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Descripción:** Exporta todas las facturas de clientes o proveedores a un archivo PDF.

### Importar Datos

#### Importar Facturas desde CSV

- **URL:** `/api/auth/importar-facturas-csv/`
- **Método:** `POST`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Cuerpo de la solicitud:** Archivo CSV en el campo `file`.
- **Descripción:** Importa facturas de clientes o proveedores desde un archivo CSV.

#### Importar Facturas desde Excel

- **URL:** `/api/auth/importar-facturas-excel/`
- **Método:** `POST`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Cuerpo de la solicitud:** Archivo Excel en el campo `file`.
- **Descripción:** Importa facturas de clientes o proveedores desde un archivo Excel.

### Exportar Facturas Individuales

#### Exportar Factura a Excel

- **URL:** `/api/auth/exportar-factura-excel/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
  - `id`: ID de la factura
- **Descripción:** Exporta una factura específica de cliente o proveedor a un archivo Excel.

#### Exportar Factura a PDF

- **URL:** `/api/auth/exportar-factura-pdf/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
  - `id`: ID de la factura
- **Descripción:** Exporta una factura específica de cliente o proveedor a un archivo PDF.

### Exportar Todas las Facturas

#### Exportar Todas las Facturas a Excel

- **URL:** `/api/auth/exportar-todas-facturas-excel/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Descripción:** Exporta todas las facturas de clientes o proveedores a un archivo Excel.

#### Exportar Todas las Facturas a PDF

- **URL:** `/api/auth/exportar-todas-facturas-pdf/`
- **Método:** `GET`
- **Parámetros de consulta:**
  - `tipo`: `cliente` o `proveedor` (por defecto: `cliente`)
- **Descripción:** Exporta todas las facturas de clientes o proveedores a un archivo PDF.

## Ejemplos de Uso

### Exportar Datos a Excel

```sh
curl -X GET "http://127.0.0.1:8000/api/auth/exportar-datos-excel/?tipo=cliente" -H "Authorization: Bearer <tu_token>"