### README: Uso de Endpoints de la API

Este documento detalla cómo utilizar los endpoints de la API para manejar usuarios, facturas de clientes y proveedores, así como el sistema de autenticación.  

---

## **Índice**
1. [Requisitos](#requisitos)
2. [Autenticación](#autenticación)
3. [Endpoints de Usuarios](#endpoints-de-usuarios)
4. [Endpoints de Facturas de Clientes](#endpoints-de-facturas-de-clientes)
5. [Endpoints de Facturas de Proveedores](#endpoints-de-facturas-de-proveedores)
6. [Roles y Permisos](#roles-y-permisos)

---

### **Requisitos**
- Python 3.8+
- Framework Django con Django REST Framework
- Cliente HTTP como Postman o cURL para probar los endpoints

---

### **Autenticación**
#### **Login**
**POST `/login/`**

- **Descripción**: Genera un token de acceso y refresco para el usuario.
- **Body (JSON)**:
  ```json
  {
    "email": "usuario@example.com",
    "contraseña": "password123"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "refresh": "<token_refresh>",
    "access": "<token_access>",
    "rol": "admin",
    "nombre": "Nombre del Usuario"
  }
  ```
- **Errores comunes**: 
  - 400: Credenciales inválidas

#### **Logout**
**POST `/logout/`**

- **Descripción**: Invalida la sesión del usuario.  
- **Respuesta (200)**:
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

### **Endpoints de Usuarios**
#### **Acceso solo para administradores**
**GET `/admin-only/`**

- **Descripción**: Endpoint restringido a usuarios con rol de administrador.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Respuesta (200)**:
  ```json
  {
    "mensaje": "Acceso solo para administradores."
  }
  ```
---

### **Endpoints de Facturas de Clientes**

#### **Obtener todas las facturas**
**GET `/facturas-clientes/`**

- **Descripción**: Lista todas las facturas de clientes.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Respuesta (200)**:
  ```json
  [
    {
      "id": 1,
      "numero_factura": "F123",
      "estado": "pendiente",
      "fecha_vencimiento": "2024-12-01"
    }
  ]
  ```

#### **Cambiar estado de una factura**
**PATCH `/facturas-clientes/{id}/cambiar_estado/`**

- **Descripción**: Cambia el estado de una factura específica.
- **Body (JSON)**:
  ```json
  {
    "estado": "pagada"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "mensaje": "Estado cambiado a pagada"
  }
  ```

#### **Notificaciones de facturas**
**GET `/facturas-clientes/notificaciones/`**

- **Descripción**: Devuelve facturas próximas a vencer y vencidas.
- **Respuesta (200)**:
  ```json
  {
    "proximas_a_vencer": [
      {
        "id": 2,
        "numero_factura": "F124",
        "fecha_vencimiento": "2024-12-03"
      }
    ],
    "vencidas": [
      {
        "id": 1,
        "numero_factura": "F123",
        "fecha_vencimiento": "2024-11-20"
      }
    ]
  }
  ```

---

### **Endpoints de Facturas de Proveedores**

#### **Obtener todas las facturas**
**GET `/facturas-proveedores/`**

- **Descripción**: Lista todas las facturas de proveedores.
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Respuesta (200)**:
  ```json
  [
    {
      "id": 1,
      "numero_factura": "P001",
      "estado": "pendiente",
      "fecha_vencimiento": "2024-11-25"
    }
  ]
  ```

#### **Cambiar estado de una factura**
**PATCH `/facturas-proveedores/{id}/cambiar_estado/`**

- **Descripción**: Cambia el estado de una factura específica.
- **Body (JSON)**:
  ```json
  {
    "estado": "cancelada"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "mensaje": "Estado cambiado a cancelada"
  }
  ```

#### **Notificaciones de facturas**
**GET `/facturas-proveedores/notificaciones/`**

- **Descripción**: Devuelve facturas próximas a vencer y vencidas.
- **Respuesta (200)**:
  ```json
  {
    "proximas_a_vencer": [
      {
        "id": 3,
        "numero_factura": "P003",
        "fecha_vencimiento": "2024-12-02"
      }
    ],
    "vencidas": [
      {
        "id": 1,
        "numero_factura": "P001",
        "fecha_vencimiento": "2024-11-20"
      }
    ]
  }
  ```

---

### **Roles y Permisos**

| Rol         | Permisos                                      |
|-------------|-----------------------------------------------|
| `admin`     | Acceso total, incluyendo creación y gestión.  |
| `contador`  | Gestión de facturas de clientes y proveedores.|
| `gerente`   | Visualización y reportes.                    |

---

**Autor**: *Tu equipo de desarrollo*  
**Contacto**: support@tudominio.com
