# 🧩 SISTEMA DE GESTIÓN EXTINSIA  
### Mini Proyecto – Sistema de Tickets con Productos y Extintores

---

## 📋 Requerimientos Funcionales

| **ID** | **Requerimiento** |
|:-------|:------------------|
| **RF01** | Autenticación de usuarios – Login y registro obligatorio antes de acceder al sistema |

# 🧩 Autenticación de Usuarios

**Como** usuario del sistema,  
**quiero** registrarme con un perfil único o iniciar sesión con mis credenciales  
**para** acceder de forma segura al sistema de gestión integral y poder realizar operaciones sobre clientes, productos, extintores y tickets.

El acceso al menú principal solo será posible después de una autenticación exitosa.  
Cualquier intento de uso sin estar logueado debe redirigir a la pantalla de inicio de sesión/registro.

---

## ✅ Criterios de Aceptación

1. El sistema muestra una pantalla inicial con las opciones: **Iniciar sesión**, **Crear cuenta** y **Salir**.  
2. Al seleccionar **Crear cuenta**, se solicitan: **nombre completo**, **email** y **contraseña** (mínimo 4 caracteres).  
3. El **email debe ser único** en el sistema. Si ya existe, se muestra: `"El email ya está registrado"`.  
4. La **contraseña se encripta con bcrypt** antes de guardarse. Nunca se almacena en texto plano.  
5. Al crear la cuenta exitosamente, se genera un código automático `USR-X` y el usuario es logueado automáticamente.  
6. Al seleccionar **Iniciar sesión**, se solicitan **email** y **contraseña**.  
7. Si las credenciales son correctas, se muestra `"¡Bienvenido, [Nombre]!"` y se accede al menú principal.  
8. Si las credenciales son incorrectas, se muestra `"Email o contraseña incorrectos"` y se permite reintentar.  
9. No se permite acceder al menú principal (ni a ninguna funcionalidad) sin estar autenticado.  
10. Desde el menú principal, debe existir una opción para **cerrar sesión**, que regresa a la pantalla inicial.  
11. Todos los **mensajes de error** son claros, en español y no exponen información técnica.  
12. El sistema **crea automáticamente** el archivo `data/usuarios.json` si no existe al intentar registrar el primer usuario.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Inicio del Sistema] --> B["Pantalla de Bienvenida"]
    
    B --> C{¿Qué desea hacer?}
    C -->|1. Iniciar sesión| D["Ingresar email y contraseña"]
    C -->|2. Crear cuenta| E["Ingresar nombre, email y contraseña"]
    C -->|0. Salir| Z[Fin del Programa]

    %% === LOGIN ===
    D --> F{¿Credenciales válidas?}
    F -->|Sí| G["Bienvenido → Menú Principal"]
    F -->|No| H["Error: Email o contraseña incorrectos"]
    H --> D

    %% === REGISTRO ===
    E --> I{¿Datos válidos?}
    I -->|No| J["Error: Campo obligatorio / formato inválido"]
    J --> E

    I -->|Sí| K{¿Email ya existe?}
    K -->|Sí| L["Error: El email ya está registrado"]
    L --> E
    K -->|No| M["Cuenta creada → USR-X"]
    M --> G

    %% === MENÚ PRINCIPAL ===
    G --> N["Menú Principal: Gestión de Clientes, Tickets, etc."]
    N --> O{¿Cerrar sesión?}
    O -->|Sí| P["Sesión cerrada"]
    P --> B
    O -->|No| N

    %% Estilos
    style A fill:#4CAF50, color:white
    style Z fill:#f44336, color:white
    style G fill:#2196F3, color:white
    style H fill:#FF9800, color:white
    style J fill:#FF9800, color:white
    style L fill:#FF9800, color:white
```

| **RF02** | Gestión de usuarios – Crear, actualizar, cambiar contraseña, eliminar cuenta |

# 🧩 Gestión de Usuarios (CRUD)

**Como** usuario autenticado,  
**quiero** modificar mis datos, contraseña y eliminar mi cuenta,  
**para** mantener mi perfil seguro y actualizado.

---

## ✅ Criterios de Aceptación

1. El menú **"Gestión de Usuarios"** solo es visible si el usuario está logueado.  
2. Se muestra el **nombre** y **email** del usuario actual.  
3. Opciones disponibles: **Actualizar datos**, **Cambiar contraseña**, **Eliminar cuenta**, **Cerrar sesión**.  
4. **Actualizar datos:** permite cambiar nombre y email (el email debe ser único).  
5. **Cambiar contraseña:** valida la contraseña actual, requiere nueva ≥ 4 caracteres y confirmación.  
6. **Eliminar cuenta:** solicita confirmación con “s” + contraseña actual → elimina permanentemente.  
7. **Cerrar sesión:** regresa a la pantalla de inicio de sesión.  
8. Todos los cambios se guardan en `data/usuarios.json`.  
9. Se realiza manejo seguro de errores (archivo vacío, corrupto, etc.).  
10. Todos los mensajes son claros, en español y sin información técnica.  
11. El código de usuario `USR-X` **no cambia nunca**.  
12. Al eliminar un usuario, su **email queda libre** para un nuevo registro.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario Logueado] --> B["Menú: Gestión de Usuarios"]
    B --> C{"Seleccione opción"}
    
    C -->|1. Actualizar datos| D["Mostrar datos actuales"]
    D --> E["Ingresar nuevo nombre (opcional)"]
    E --> F["Ingresar nuevo email (opcional)"]
    F --> G{¿Email nuevo ya existe?}
    G -->|Sí| H["Error: Email ya registrado"]
    G -->|No| I["Actualizar en usuarios.json"]
    I --> J["Éxito → Volver al menú"]
    H --> J

    C -->|2. Cambiar contraseña| K["Ingresar contraseña actual"]
    K --> L{¿Contraseña actual correcta?}
    L -->|No| M["Error: Contraseña incorrecta"]
    L -->|Sí| N["Ingresar nueva contraseña"]
    N --> O["Confirmar nueva contraseña"]
    O --> P{¿Coinciden y ≥4 caracteres?}
    P -->|No| Q["Error: Contraseñas no coinciden o muy corta"]
    P -->|Sí| R["Encriptar y guardar"]
    R --> S["Éxito → Volver al menú"]
    M --> S
    Q --> S

    C -->|3. Eliminar cuenta| T["¿Eliminar 'juan@example.com'? (s/N)"]
    T -->|No| U["Operación cancelada → Volver"]
    T -->|Sí| V["Ingresar contraseña actual"]
    V --> W{¿Contraseña correcta?}
    W -->|No| X["Error: Contraseña incorrecta"]
    W -->|Sí| Y["Eliminar usuario del JSON"]
    Y --> Z["Sesión cerrada → Pantalla de inicio"]
    X --> U
    U --> C

    C -->|4. Cerrar sesión| AA["¿Cerrar sesión? (s/N)"]
    AA -->|No| AB["Volver al menú"]
    AA -->|Sí| AC["Sesión cerrada → Pantalla de inicio"]
    AB --> C

    C -->|0. Volver| AD["Regresar al Menú Principal"]

    %% Estilos
    style A fill:#2196F3, color:white
    style Z fill:#4CAF50, color:white
    style AC fill:#4CAF50, color:white
    style H fill:#FF9800, color:white
    style M fill:#FF9800, color:white
    style Q fill:#FF9800, color:white
    style X fill:#FF9800, color:white
    style J fill:#8BC34A, color:white
    style S fill:#8BC34A, color:white
```

| **RF03** | Gestión de clientes – CRUD completo con búsqueda por nombre y vencimiento |

# 🧩 Gestión de Clientes

**Como** usuario autenticado (técnico o administrador),  
**quiero** crear, ver, actualizar y eliminar clientes, además de buscarlos por nombre o mes de vencimiento,  
**para** mantener un registro organizado y actualizado de los clientes del servicio.

---

## ✅ Criterios de Aceptación

1. El menú **"Gestión de Clientes"** solo es accesible si el usuario está logueado.  
2. Opciones disponibles: **Crear**, **Listar**, **Buscar por nombre**, **Buscar por vencimiento**, **Actualizar**, **Eliminar**.  
3. **Crear:** valida nombre de empresa (única), nombre del encargado, celular (10 dígitos), dirección y mes válido.  
4. Se genera un código automático `CLI-1`, `CLI-2`, etc.  
5. **Listar:** muestra código, empresa, celular y mes de vencimiento.  
6. **Buscar por nombre:** realiza una búsqueda parcial (insensible a mayúsculas) en empresa o encargado.  
7. **Buscar por vencimiento:** filtra clientes cuyo mes de vencimiento coincide.  
8. **Actualizar:** permite modificar cualquier campo (valida duplicados en el nombre de empresa).  
9. **Eliminar:** solicita confirmación con “s” + código → elimina permanentemente.  
10. Todos los datos se guardan en `data/clientes.json`.  
11. Si el archivo está vacío o no existe, se maneja como `[]` sin error.  
12. Los mensajes del sistema son claros y en español, por ejemplo: `"Cliente creado"`, `"No se encontraron resultados"`, etc.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario Logueado] --> B["Menú: Gestión de Clientes"]
    B --> C{"Seleccione opción"}

    %% === CREAR ===
    C -->|1. Crear cliente| D["Ingresar: empresa, encargado, dirección, celular, mes"]
    D --> E{¿Datos válidos?}
    E -->|No| F["Error: campo obligatorio, formato o duplicado"]
    E -->|Sí| G["Generar CLI-X"]
    G --> H["Guardar en clientes.json"]
    H --> I["Éxito → Volver"]
    F --> I

    %% === LISTAR ===
    C -->|2. Listar todos| J{"¿Hay clientes?"}
    J -->|No| K["No hay clientes registrados"]
    J -->|Sí| L["Mostrar: código | empresa | celular | mes"]
    L --> I
    K --> I

    %% === BUSCAR NOMBRE ===
    C -->|3. Buscar por nombre| M["Ingrese texto a buscar"]
    M --> N["Buscar en empresa y encargado (insensible)"]
    N --> O{"¿Resultados?"}
    O -->|No| P["No se encontraron clientes"]
    O -->|Sí| Q["Mostrar resultados"]
    Q --> I
    P --> I

    %% === POR VENCIMIENTO ===
    C -->|4. Clientes por vencimiento| R["Ingrese mes (ej: Agosto)"]
    R --> S{¿Mes válido?}
    S -->|No| T["Mes inválido"]
    S -->|Sí| U["Filtrar clientes con ese mes"]
    U --> V{"¿Hay coincidencias?"}
    V -->|No| W["Ningún cliente vence en [mes]"]
    V -->|Sí| X["Mostrar lista"]
    X --> I
    T --> I
    W --> I

    %% === ACTUALIZAR ===
    C -->|5. Actualizar cliente| Y["Ingrese código del cliente"]
    Y --> Z{"¿Existe?"}
    Z -->|No| AA["Cliente no encontrado"]
    Z -->|Sí| AB["Mostrar datos actuales"]
    AB --> AC["Ingresar nuevos valores (opcionales)"]
    AC --> AD{¿Empresa duplicada?}
    AD -->|Sí| AE["Ya existe otro cliente con ese nombre"]
    AD -->|No| AF["Actualizar en JSON"]
    AF --> AG["Éxito → Volver"]
    AA --> I
    AE --> I

    %% === ELIMINAR ===
    C -->|6. Eliminar cliente| AH["Ingrese código"]
    AH --> AI{"¿Existe?"}
    AI -->|No| AJ["Cliente no encontrado"]
    AI -->|Sí| AK["¿Eliminar CLI-X? (s/N)"]
    AK -->|No| AL["Operación cancelada"]
    AK -->|Sí| AM["Eliminar del JSON"]
    AM --> AN["Éxito → Volver"]
    AJ --> I
    AL --> I

    %% === VOLVER ===
    C -->|0. Volver| AO["Regresar al Menú Principal"]

    %% === ESTILOS ===
    style A fill:#2196F3, color:white
    style I fill:#8BC34A, color:white
    style F fill:#FF9800, color:white
    style K fill:#FF9800, color:white
    style P fill:#FF9800, color:white
    style T fill:#FF9800, color:white
    style W fill:#FF9800, color:white
    style AA fill:#FF9800, color:white
    style AE fill:#FF9800, color:white
    style AJ fill:#FF9800, color:white
```

| **RF04** | Gestión de productos – CRUD con búsqueda por nombre y precio |

# 🧩 Gestión de Productos

**Como** usuario autenticado (técnico o administrador),  
**quiero** crear, ver, actualizar y eliminar productos, además de buscarlos por nombre o rango de precio,  
**para** mantener un catálogo actualizado de los productos disponibles en el sistema.

---

## ✅ Criterios de Aceptación

1. El menú **"Gestión de Productos"** solo es accesible si el usuario está logueado.  
2. Opciones disponibles: **Crear**, **Listar**, **Buscar por nombre**, **Buscar por precio**, **Actualizar**, **Eliminar**.  
3. **Crear:** valida nombre (único) y que el precio sea mayor que 0.  
4. Se genera un código automático `PRO-1`, `PRO-2`, etc.  
5. **Listar:** muestra código, nombre y precio.  
6. **Buscar por nombre:** realiza una búsqueda parcial (insensible a mayúsculas).  
7. **Buscar por precio:** permite filtrar por rango opcional (mínimo y/o máximo).  
8. **Actualizar:** permite modificar nombre (único) y precio.  
9. **Eliminar:** solicita confirmación con “s” + código → elimina permanentemente.  
10. Todos los datos se guardan en `data/productos.json`.  
11. Si el archivo está vacío o no existe, se maneja como `[]` sin error.  
12. Los mensajes del sistema son claros y en español, por ejemplo: `"Producto creado"`, `"No encontrado"`, etc.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario Logueado] --> B["Menú: Gestión de Productos"]
    B --> C{"Seleccione opción"}

    %% === CREAR ===
    C -->|1. Crear producto| D["Ingresar: nombre, precio"]
    D --> E{¿Nombre vacío o precio ≤0?}
    E -->|Sí| F["Error: nombre obligatorio, precio > 0"]
    E -->|No| G{¿Nombre ya existe?}
    G -->|Sí| H["Error: Ya existe un producto con ese nombre"]
    G -->|No| I["Generar PRO-X"]
    I --> J["Guardar en productos.json"]
    J --> K["Éxito → Volver"]
    F --> K
    H --> K

    %% === LISTAR ===
    C -->|2. Listar todos| L{"¿Hay productos?"}
    L -->|No| M["No hay productos registrados"]
    L -->|Sí| N["Mostrar: código | nombre | precio"]
    N --> K
    M --> K

    %% === BUSCAR NOMBRE ===
    C -->|3. Buscar por nombre| O["Ingrese texto a buscar"]
    O --> P["Búsqueda parcial (insensible)"]
    P --> Q{"¿Resultados?"}
    Q -->|No| R["No se encontraron productos"]
    Q -->|Sí| S["Mostrar resultados"]
    S --> K
    R --> K

    %% === BUSCAR PRECIO ===
    C -->|4. Buscar por precio| T["Ingrese precio mínimo"]
    T --> U["Precio máximo (opcional)"]
    U --> V["Filtrar por rango"]
    V --> W{"¿Resultados?"}
    W -->|No| X["No hay productos en ese rango"]
    W -->|Sí| Y["Mostrar: código | nombre | precio"]
    Y --> K
    X --> K

    %% === ACTUALIZAR ===
    C -->|5. Actualizar producto| Z["Ingrese código"]
    Z --> AA{"¿Existe?"}
    AA -->|No| AB["Producto no encontrado"]
    AA -->|Sí| AC["Mostrar datos actuales"]
    AC --> AD["Ingresar nuevo nombre (opcional)"]
    AD --> AE["Ingresar nuevo precio (opcional)"]
    AE --> AF{¿Nombre duplicado?}
    AF -->|Sí| AG["Ya existe otro producto con ese nombre"]
    AF -->|No| AH["Actualizar en JSON"]
    AH --> AI["Éxito → Volver"]
    AB --> K
    AG --> K

    %% === ELIMINAR ===
    C -->|6. Eliminar producto| AJ["Ingrese código"]
    AJ --> AK{"¿Existe?"}
    AK -->|No| AL["Producto no encontrado"]
    AK -->|Sí| AM["¿Eliminar PRO-X? (s/N)"]
    AM -->|No| AN["Operación cancelada"]
    AM -->|Sí| AO["Eliminar del JSON"]
    AO --> AP["Éxito → Volver"]
    AL --> K
    AN --> K

    %% === VOLVER ===
    C -->|0. Volver| AQ["Regresar al Menú Principal"]

    %% === ESTILOS ===
    style A fill:#2196F3, color:white
    style K fill:#8BC34A, color:white
    style F fill:#FF9800, color:white
    style H fill:#FF9800, color:white
    style M fill:#FF9800, color:white
    style R fill:#FF9800, color:white
    style X fill:#FF9800, color:white
    style AB fill:#FF9800, color:white
    style AG fill:#FF9800, color:white
    style AL fill:#FF9800, color:white
```

| **RF05** | Gestión de extintores – CRUD con búsqueda por tipo y capacidad |

# 🧩 Gestión de Extintores

**Como** usuario autenticado (técnico o administrador),  
**quiero** crear, ver, actualizar y eliminar extintores, además de buscarlos por tipo o rango de capacidad,  
**para** mantener un catálogo organizado de extintores disponibles para venta o servicio.

---

## ✅ Criterios de Aceptación

1. El menú **"Gestión de Extintores"** solo es accesible si el usuario está logueado.  
2. Opciones disponibles: **Crear**, **Listar**, **Buscar por tipo**, **Buscar por capacidad**, **Actualizar**, **Eliminar**.  
3. **Crear:** valida nombre, precio (> 0), tipo (ejemplo: `CO2`, `ABC`), y capacidad (> 0).  
4. Se genera un código automático `EXT-1`, `EXT-2`, etc.  
5. **Listar:** muestra código, nombre, tipo, capacidad y precio.  
6. **Buscar por tipo:** aplica un filtro exacto (insensible a mayúsculas).  
7. **Buscar por capacidad:** permite buscar por rango opcional (mínimo y/o máximo).  
8. **Actualizar:** permite modificar cualquier campo del extintor.  
9. **Eliminar:** solicita confirmación con “s” + código → elimina permanentemente.  
10. Todos los datos se guardan en `data/extintores.json`.  
11. Si el archivo está vacío o no existe, se maneja como `[]` sin error.  
12. Los mensajes del sistema son claros y en español, por ejemplo: `"Extintor creado"`, `"No encontrado"`, etc.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario Logueado] --> B["Menú: Gestión de Extintores"]
    B --> C{"Seleccione opción"}

    %% === CREAR ===
    C -->|1. Crear extintor| D["Ingresar: nombre, precio, tipo, capacidad"]
    D --> E{¿Datos válidos?}
    E -->|No| F["Error: nombre, precio>0, tipo, capacidad>0"]
    E -->|Sí| G["Generar EXT-X"]
    G --> H["Guardar en extintores.json"]
    H --> I["Éxito → Volver"]
    F --> I

    %% === LISTAR ===
    C -->|2. Listar todos| J{"¿Hay extintores?"}
    J -->|No| K["No hay extintores registrados"]
    J -->|Sí| L["Mostrar: código | nombre | tipo | cap | precio"]
    L --> I
    K --> I

    %% === BUSCAR TIPO ===
    C -->|3. Buscar por tipo| M["Ingrese tipo (ej: CO2)"]
    M --> N["Filtrar por tipo (insensible)"]
    N --> O{"¿Resultados?"}
    O -->|No| P["No se encontraron extintores de ese tipo"]
    O -->|Sí| Q["Mostrar resultados"]
    Q --> I
    P --> I

    %% === BUSCAR CAPACIDAD ===
    C -->|4. Buscar por capacidad| R["Capacidad mínima (kg)"]
    R --> S["Capacidad máxima (opcional)"]
    S --> T["Filtrar por rango"]
    T --> U{"¿Resultados?"}
    U -->|No| V["No hay extintores en ese rango"]
    U -->|Sí| W["Mostrar: código | nombre | capacidad | precio"]
    W --> I
    V --> I

    %% === ACTUALIZAR ===
    C -->|5. Actualizar extintor| X["Ingrese código"]
    X --> Y{"¿Existe?"}
    Y -->|No| Z["Extintor no encontrado"]
    Y -->|Sí| AA["Mostrar datos actuales"]
    AA --> AB["Ingresar nuevos valores (opcionales)"]
    AB --> AC{¿Datos válidos?}
    AC -->|No| AD["Error: precio>0, capacidad>0"]
    AC -->|Sí| AE["Actualizar en JSON"]
    AE --> AF["Éxito → Volver"]
    Z --> I
    AD --> I

    %% === ELIMINAR ===
    C -->|6. Eliminar extintor| AG["Ingrese código"]
    AG --> AH{"¿Existe?"}
    AH -->|No| AI["Extintor no encontrado"]
    AH -->|Sí| AJ["¿Eliminar EXT-X? (s/N)"]
    AJ -->|No| AK["Operación cancelada"]
    AJ -->|Sí| AL["Eliminar del JSON"]
    AL --> AM["Éxito → Volver"]
    AI --> I
    AK --> I

    %% === VOLVER ===
    C -->|0. Volver| AN["Regresar al Menú Principal"]

    %% === ESTILOS ===
    style A fill:#2196F3, color:white
    style I fill:#8BC34A, color:white
    style F fill:#FF9800, color:white
    style K fill:#FF9800, color:white
    style P fill:#FF9800, color:white
    style V fill:#FF9800, color:white
    style Z fill:#FF9800, color:white
    style AD fill:#FF9800, color:white
    style AI fill:#FF9800, color:white
```

| **RF06** | Gestión de tickets – Crear ticket con productos y extintores, listar, filtrar por cliente |

# 🧩 Gestión de Tickets

**Como** técnico autenticado,  
**quiero** crear tickets que incluyan productos y extintores, ver todos los tickets y filtrarlos por cliente,  
**para** registrar servicios realizados y tener trazabilidad de ventas por cliente.

---

## ✅ Criterios de Aceptación

1. El menú **"Gestión de Tickets"** solo es accesible si el usuario está logueado.  
2. Opciones disponibles: **Crear**, **Listar todos**, **Ver por cliente**, **Actualizar**, **Eliminar**.  
3. **Crear:** solicita servicio, código de cliente y lista de productos/extintores (código + cantidad).  
4. Se valida que el cliente, los productos y los extintores existan antes de guardar.  
5. Sincroniza nombre y precio desde `ProductosRepo` o `ExtintoresRepo`.  
6. Se genera un código automático `TIC-1`, `TIC-2`, etc.  
7. Calcula el **total = Σ(precio × cantidad)**.  
8. Guarda la **fecha actual** en formato `YYYY-MM-DD`.  
9. **Listar todos:** muestra código, cliente, total y fecha.  
10. **Filtrar por cliente:** muestra todos los tickets correspondientes a un código de cliente.  
11. **Actualizar:** permite modificar el servicio o la lista de productos/extintores.  
12. **Eliminar:** solicita confirmación con “s” + código → elimina permanentemente.  
13. Todos los datos se guardan en `data/tickets.json`.  
14. Los mensajes del sistema son claros y en español, por ejemplo: `"Ticket creado: TIC-5"`.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario Logueado] --> B["Menú: Gestión de Tickets"]
    B --> C{"Seleccione opción"}

    %% === CREAR TICKET ===
    C -->|1. Crear ticket| D["Ingresar servicio"]
    D --> E["Ingresar código cliente"]
    E --> F{"¿Cliente existe?"}
    F -->|No| G["Error: Cliente no encontrado"]
    F -->|Sí| H["Ingresar productos/extintores"]
    H --> I["Código + Cantidad (fin para terminar)"]
    I --> J{"¿Código válido?"}
    J -->|No| K["Error: Código no existe en productos ni extintores"]
    J -->|Sí| L["Sincronizar nombre y precio"]
    L --> M{"¿Más ítems?"}
    M -->|Sí| I
    M -->|No| N["Calcular total"]
    N --> O["Generar TIC-X + Fecha actual"]
    O --> P["Guardar en tickets.json"]
    P --> Q["Éxito: Ticket creado | Total: $X"]
    G --> R["Volver"]
    K --> R

    %% === LISTAR TODOS ===
    C -->|2. Listar todos| S{"¿Hay tickets?"}
    S -->|No| T["No hay tickets registrados"]
    S -->|Sí| U["Mostrar: código | cliente | total | fecha"]
    U --> R
    T --> R

    %% === POR CLIENTE ===
    C -->|3. Ver por cliente| V["Ingresar código cliente"]
    V --> W{"¿Cliente existe?"}
    W -->|No| X["Cliente no encontrado"]
    W -->|Sí| Y{"¿Tiene tickets?"}
    Y -->|No| Z["No hay tickets para este cliente"]
    Y -->|Sí| AA["Mostrar lista de tickets"]
    AA --> R
    X --> R
    Z --> R

    %% === ACTUALIZAR ===
    C -->|4. Actualizar ticket| AB["Ingresar código ticket"]
    AB --> AC{"¿Existe?"}
    AC -->|No| AD["Ticket no encontrado"]
    AC -->|Sí| AE["Modificar servicio (opcional)"]
    AE --> AF["¿Actualizar productos? (s/N)"]
    AF -->|No| AG["Guardar cambios"]
    AF -->|Sí| H
    AG --> AH["Éxito → Volver"]
    AD --> R

    %% === ELIMINAR ===
    C -->|5. Eliminar ticket| AI["Ingresar código"]
    AI --> AJ{"¿Existe?"}
    AJ -->|No| AK["Ticket no encontrado"]
    AJ -->|Sí| AL["¿Eliminar TIC-X? (s/N)"]
    AL -->|No| AM["Operación cancelada"]
    AL -->|Sí| AN["Eliminar del JSON"]
    AN --> AO["Éxito → Volver"]
    AK --> R
    AM --> R

    %% === VOLVER ===
    C -->|0. Volver| AP["Regresar al Menú Principal"]

    %% === ESTILOS ===
    style A fill:#2196F3, color:white
    style R fill:#8BC34A, color:white
    style Q fill:#8BC34A, color:white
    style AH fill:#8BC34A, color:white
    style AO fill:#8BC34A, color:white
    style G fill:#FF9800, color:white
    style K fill:#FF9800, color:white
    style T fill:#FF9800, color:white
    style X fill:#FF9800, color:white
    style Z fill:#FF9800, color:white
    style AD fill:#FF9800, color:white
    style AK fill:#FF9800, color:white
```

| **RF07** | Sincronización de catálogo – Precio y nombre de productos/extintores se toman del catálogo al crear ticket |

# 🧩 Sincronización de Catálogo en Tickets

**Como** técnico,  
**quiero** que al crear un ticket, los productos y extintores se sincronicen automáticamente con el catálogo,  
**para** garantizar que el nombre y precio del ticket sean siempre correctos y actualizados.

---

## ✅ Criterios de Aceptación

1. Al crear un ticket, se solicita el **código** y la **cantidad** de cada ítem.  
2. El sistema busca primero en `ProductosRepo` por el código proporcionado.  
3. Si no lo encuentra, busca en `ExtintoresRepo`.  
4. Si el ítem existe en cualquiera de los dos repositorios, se **sincroniza automáticamente** su nombre y precio con el catálogo actual.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Crear Ticket] --> B["Ingresar código + cantidad"]
    B --> C{"¿Código ingresado?"}
    C -->|Sí| D["Buscar en ProductosRepo"]
    D --> E{"¿Encontrado?"}
    E -->|Sí| F["Sincronizar: nombre y precio desde Producto"]
    E -->|No| G["Buscar en ExtintoresRepo"]
    G --> H{"¿Encontrado?"}
    H -->|Sí| I["Sincronizar: nombre y precio desde Extintor"]
    H -->|No| J["Error: Código no existe en catálogo"]
    J --> K["Volver a ingresar código"]
    F --> L["Agregar a lista sincronizada"]
    I --> L
    L --> M{"¿Más ítems?"}
    M -->|Sí| B
    M -->|No| N["Calcular total"]
    N --> O["Guardar ticket con datos sincronizados"]
    O --> P["Éxito: Ticket creado"]
    C -->|"No (fin)"| N

    %% Estilos
    style A fill:#2196F3, color:white
    style P fill:#8BC34A, color:white
    style J fill:#FF9800, color:white
    style F fill:#4CAF50, color:white
    style I fill:#4CAF50, color:white
    style L fill:#81C784, color:white
```

| **RF08** | Validación de datos – Campos obligatorios, formatos, duplicados |

# 🧩 Validación de Datos en Todo el Sistema

**Como** usuario del sistema,  
**quiero** que todos los datos ingresados sean validados automáticamente,  
**para** evitar errores, inconsistencias y datos corruptos en el sistema.

---

## ✅ Criterios de Aceptación

1. Los **campos obligatorios** no pueden estar vacíos (por ejemplo: nombre, email, empresa, etc.).  
2. El **email** debe tener un formato válido (`usuario@dominio.com`).  
3. El **celular** debe contener exactamente **10 dígitos numéricos**.  
4. El **precio** debe ser un **número positivo** (> 0).  
5. La **capacidad** también debe ser un **número positivo** (> 0).  
6. El **mes de vencimiento** debe corresponder a uno de los **12 meses válidos** del año.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario ingresa datos] --> B["Aplicar validaciones"]
    
    B --> C{"¿Campo obligatorio vacío?"}
    C -->|Oui| D["Error: Campo obligatorio"]
    C -->|No| E{"¿Email inválido?"}
    E -->|Oui| F["Error: Formato de email incorrecto"]
    E -->|No| G{"¿Celular no tiene 10 dígitos?"}
    G -->|Oui| H["Error: Celular debe tener 10 dígitos"]
    G -->|No| I{"¿Precio ≤ 0?"}
    I -->|Oui| J["Error: Precio debe ser mayor a 0"]
    I -->|No| K{"¿Capacidad ≤ 0?"}
    K -->|Oui| L["Error: Capacidad debe ser mayor a 0"]
    K -->|No| M{"¿Mes inválido?"}
    M -->|Oui| N["Error: Mes no válido (use: Enero, ... Diciembre)"]
    M -->|No| O{"¿Duplicado (email/empresa/producto)?"}
    O -->|Oui| P["Error: Ya existe un registro con ese valor"]
    O -->|No| Q{"¿Contraseña < 4 caracteres?"}
    Q -->|Oui| R["Error: Contraseña muy corta"]
    Q -->|No| S["Datos válidos"]
    
    S --> T["Guardar en JSON"]
    T --> U["Éxito: Operación completada"]
    
    D --> V["Reintentar ingreso"]
    F --> V
    H --> V
    J --> V
    L --> V
    N --> V
    P --> V
    R --> V
    
    V --> A

    %% Estilos
    style A fill:#2196F3, color:white
    style U fill:#4CAF50, color:white
    style T fill:#81C784, color:white
    style D fill:#FF9800, color:white
    style F fill:#FF9800, color:white
    style H fill:#FF9800, color:white
    style J fill:#FF9800, color:white
    style L fill:#FF9800, color:white
    style N fill:#FF9800, color:white
    style P fill:#FF9800, color:white
    style R fill:#FF9800, color:white
```

| **RF09** | Códigos únicos automáticos – `USR-1`, `CLI-1`, `PRO-1`, `EXT-1`, `TIC-1` |

# 🧩 Generación Automática de Códigos Únicos

**Como** usuario del sistema,  
**quiero** que todos los registros tengan un código único generado automáticamente,  
**para** identificar fácilmente cada registro sin intervención manual ni riesgo de duplicados.

---

## ✅ Criterios de Aceptación

1. El **formato** del código debe seguir la estructura `TIPO-NÚMERO` (por ejemplo: `USR-1`, `CLI-5`, `PRO-23`).  
2. Cada entidad tiene un **prefijo único**:  
   - `USR-` → Usuarios  
   - `CLI-` → Clientes  
   - `PRO-` → Productos  
   - `EXT-` → Extintores  
   - `TIC-` → Tickets  
3. La generación del código es **automática**: el usuario **no puede ingresarlo manualmente**.  
4. El número es **incremental**, asignando siempre el **siguiente número disponible**.  
5. Los códigos son **persistentes**, conservándose incluso tras reiniciar el sistema.  
6. Cada código es **inmutable**, no se modifica al actualizar un registro.  
7. Los códigos son **únicos globalmente**, sin posibilidad de duplicados entre registros.  
8. El código se genera **antes de guardar** el registro en el archivo JSON.  
9. Si el archivo está vacío, la numeración **comienza desde 1**.  
10. Al crear un registro, el sistema muestra un mensaje como: `"Cliente creado: CLI-1"`.

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Crear Nuevo Registro] --> B["Leer archivo JSON"]
    
    B --> C{"¿Archivo existe y tiene datos?"}
    C -->|No| D["Primer registro → CÓDIGO = TIPO-1"]
    C -->|Sí| E["Buscar máximo código existente"]
    
    E --> F["Extraer números: CLI-1→1, CLI-5→5, CLI-23→23"]
    F --> G["MÁXIMO = 23"]
    G --> H["NUEVO = MÁXIMO + 1 = 24"]
    H --> I["CÓDIGO FINAL = TIPO-24"]
    
    D --> J["CÓDIGO FINAL = TIPO-1"]
    
    I --> K["Guardar en JSON con código"]
    J --> K
    
    K --> L["Mostrar: 'Cliente creado: CLI-24'"]
    L --> M[Fin]

    %% Ejemplo visual con datos
    subgraph "Ejemplo: clientes.json"
        N["CLI-1: Corona"]
        O["CLI-5: Ferretería"]
        P["CLI-23: ABC"]
    end
    
    E -.-> N
    E -.-> O
    E -.-> P

    %% Estilos
    style A fill:#2196F3, color:white
    style L fill:#4CAF50, color:white
    style M fill:#4CAF50, color:white
    style D fill:#FF9800, color:white
    style I fill:#FF9800, color:white
    style N fill:#E3F2FD
    style O fill:#E3F2FD
    style P fill:#E3F2FD
```

| **RF10** | Persistencia en JSON – Todos los datos se guardan en archivos `data/*.json` |

# 🧩 Persistencia de Datos en Archivos JSON

**Como** administrador del sistema,  
**quiero** que todos los datos (usuarios, clientes, productos, extintores, tickets) se guarden en archivos JSON,  
**para** garantizar que la información persista entre sesiones y sea fácil de respaldar.

---

## ✅ Criterios de Aceptación

1. Todos los datos se guardan en la carpeta `data/`.  
2. Archivos por entidad:  
   - `data/usuarios.json`  
   - `data/clientes.json`  
   - `data/productos.json`  
   - `data/extintores.json`  
   - `data/tickets.json`  
3. Si la carpeta `data/` no existe, el sistema la **crea automáticamente**.  
4. Si el archivo JSON no existe, se crea con una lista vacía `[]`.  
5. Si el archivo está corrupto, se trata como **vacío (`[]`)** sin que el programa falle.  
6. El formato de los archivos es **JSON válido**, con `indent=4`, `UTF-8`, y `ensure_ascii=False`.  
7. Las operaciones de lectura/escritura manejan **errores seguros**: `FileNotFoundError`, `JSONDecodeError`, etc.  
8. Los archivos **no deben editarse manualmente**; solo el sistema escribe en ellos.  
9. Los datos guardados deben incluir **todos los campos definidos en el modelo** correspondiente.  
10. Al iniciar el programa, los datos se **cargan desde los archivos JSON**.  
11. Al cerrar o modificar información, los cambios se **guardan inmediatamente**.  
12. El respaldo del sistema se realiza fácilmente copiando la carpeta `data/` com

##  📊 Diagrama de flujo

```mermaid
flowchart TD
    A[Inicio del Sistema] --> B["Verificar carpeta 'data/'"]
    B --> C{"¿Existe 'data/'?"}
    C -->|No| D["Crear carpeta 'data/'"]
    C -->|Sí| E["Continuar"]

    D --> E
    E --> F["Cargar usuarios.json"]
    F --> G{"¿Existe y es válido?"}
    G -->|No| H["Crear usuarios.json → []"]
    G -->|Sí| I["Cargar lista de usuarios"]
    H --> I

    I --> J["Repetir para: clientes, productos, extintores, tickets"]
    J --> K["Sistema listo con datos cargados"]

    %% Estilos
    style A fill:#2196F3, color:white
    style K fill:#4CAF50, color:white
    style D fill:#FF9800, color:white
    style H fill:#FF9800, color:white
```