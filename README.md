# transaction-analysis

## Introducción

El objetivo del presente proyecto es diseñar una arquitectura de bases de datos para gestionar y analizar información relacionada con pagos rechazados que derivan en devoluciones de dinero en Mercado Libre.

Por consiguiente, el propósito principal del proyecto se fundamenta en el diseño del flujo de datos, procesamiento de información e implementación de los frameworks que permiten procesar y analizar la información de transacciones rechazadas que implica devoluciones de dinero. La arquitectura propuesta considera tecnologías modernas y especializadas en el manejo de grandes volúmenes de datos, incluyendo bases de datos NoSQL como Redis (relación llave – valor) y MongoDB (estructura documental), así como modelos relacionales, donde se encuentra SQL.

Los frameworks mencionados con anterioridad han sido seleccionados porque son coherentes con el desarrollo del modelo de negocio de Mercado Libre. En primera instancia, las bases de datos no relacionales son eficientes en sistemas transaccionales, hecho que se relaciona con el modelo de negocio de Mercado Libre, donde cada usuario realiza transacciones de compra y venta de artículos en tiempo real. Por consiguiente, Redis permite acceder a la información de usuarios mediante la relación llave - valor, así mismo, el motor documental (Mongo DB) contiene la información detallada de cada usuario, sin que ello implique procesos relacionales que son ineficientes en sistemas transaccionales.  No obstante, es importante mencionar que la identificación de patrones, que en este caso son punto de partida para la identificación de eventos de fraude, se analizan mediante análisis de analítica, por consiguiente, el último framework es un motor relacional como PostgreSQL.

Cabe resaltar que la problemática de transacciones que derivan en devoluciones de dinero es un aspecto fundamental para la compañía, en primer lugar porque las devoluciones se traducen en egresos, situación que da lugar a riesgos de liquidez asociados a la gestión eficiente del flujo de caja. Por otro lado, la compañía debe garantizar el cumplimiento de la normativa de sistema de prevención de lavado de activos y financiación del terrorismo.

Por útlimo, se utiliza Next.js versión 14 en el frontend para que el cliente pueda interactuar con la herramienta. La elección se fundamenta en la capacidad de Next.js para mejorar el rendimiento y la optimización para motores de búsqueda (SEO), lo que contribuye a la accesibilidad y visibilidad del sitio web donde se desplegará la aplicación.

## Objetivos

### Objetivo general

Implementar arquitectura de bases de datos que permita gestionar información de pagos rechazados que conllevan a devoluciones de dinero en Mercado Libre, para identificar potenciales eficiencias en la gestión de liquidez, mitigación de fraude y mejora en los procesos financieros que satisfagan al cliente.
  
### Objetivos específicos

1.	Diseñar e implementar modelos de datos adecuados para la estructuración y almacenamiento eficiente de información relacionada con pagos rechazados, considerando tanto aspectos transaccionales como analíticos.

2.	Desarrollar interfaces y APIs para la ingesta de datos provenientes de diferentes fuentes, asegurando la coherencia y consistencia de la información almacenada.

3.	Integrar Next.js versión 14 en el frontend para mejorar el rendimiento y la experiencia del usuario en el sitio web, asegurando una navegación fluida y una óptima indexación en motores de búsqueda.

## Atributos de calidad

### Escalabilidad

Se toma como referencia el modelo de escalabilidad híbrido (Scale Diagonally) considerando que se utilizan motores relacionales y no relacionales. En primera instancia, para los frameworks como Redis y Mongo DB es eficiente el modelo de escalabilidad horizontal. En ese orden de ideas, en la medida que incremente el volumen transaccional, se amplía la capacidad de gestión de clústeres y nodos. 

Por su parte, la sección de base de datos relacionales se fundamenta en un modelo de escalabilidad vertical, donde se expandirá la capacidad de almacenamiento según los modelos de analítica.

### Rendimiento

El rendimiento de la arquitectura se puede medir mediante el consumo de memoria y CPU por contenedor (Docker), de igual forma, es posible monitorear los datos leídos y escritos, al igual que hacer seguimiento al performance de los contenedores mediantes los "logs".

### Disponibilidad

Mediante la configuración de nodo manager en Docker se garantiza la disponibilidad de los recursos en contenedores, por ello, en la medida que se requieran más recursos, es posible realizar agrupación de clústeres para crear un grupo cooperativo que proporcione redundancia y sostenibilidad de la arquitectura. De igual forma, permite a los administradores agregar o restar contenedores.

### Seguridad

Docker utiliza tecnologías de virtualización a nivel de sistema operativo para garantizar que cada contenedor tenga su propio entorno aislado. Esto significa que cada base de datos se ejecutará en su propio contendedor, lo que reduce el riesgo de interferencia entre ellas y evita la propagación de incidentes relacionados con inyección de código malicioso o Cross Side Scripting (XSS).

### Mantenibilidad

Docker se fundamenta en la creación de imágenes donde se realiza el desarrollo de la arquitectura. En este orden de ideas, cuando se requiere hacer mantenimiento, se realiza actualización sobre las imágenes. Además, Docker proporciona barreras de seguridad tanto para administradores como para desarrolladores mediante accesos restringidos por roles.

Dado que el rol principal que se tendrá durante la ejecución del proyecto es de desarrolladores se establecen tokens de acceso personal (PAT).

### Confiabilidad

La confiabilidad se relaciona con el punto de seguridad previamente descrito, por consiguiente, se tendrá en consideración la utilización de cuotas de recursos, garantizar la seguridad de los recursos del contenedor, usar fuente confiable como ir a la fuente del código y no ejecutar el contenedor de Docker desde la raíz. De igual forma, garantizar la independencia de los contenedores.

## Descripción de la arquitectura

Arquitectura basada en Docker para consulta e ingesta de datos de pagos rechazados. 

![image](https://github.com/Elkin77/transaction-analysis/assets/161098729/2b37fa4d-044d-4da6-8595-e2c593a66bf8)

### Componentes

#### 1. Redis

Redis es una base de datos en memoria de código abierto que se utiliza como almacén de estructuras de datos clave-valor. Es conocida por su velocidad y versatilidad, por lo que se aplica ampliamente en casos de uso, incluido el almacenamiento en caché, la gestión de sesiones, la mensajería en tiempo real, entre otros.  

Así mismo, Redis ofrece características únicas que lo hacen especialmente adecuado para gestionar el caché en eventos como el inicio de sesión. Su rendimiento, estructuras de datos específicas, capacidad de TTL, escalabilidad y facilidad de integración lo convierten en una opción sólida para mejorar el rendimiento y la eficiencia del proceso de inicio de sesión en una aplicación. 

#### 2. MongoDB

Motor de base de datos documental, al ser una base de datos no relacional basada en documentos es eficiente para el procesamiento y consulta de la información, considerando que no tiene dependencia de otras tablas ni la rigidez de la estructuras de las tablas relacionales.

#### 3. PostgresSQL

Sistema de gestión de bases de datos relacional orientado a objetos y de código abierto, ideal para soportar y crear consultas a nivel analítico para estructurar consultas a nivel negocio

#### 4. Python

Lenguaje de alto nivel de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código. programación multiparadigma, ya que soporta parcialmente la orientación a objetos, programación imperativa y, en menor medida, programación funcional. Y con notable efectividad para lectura de archivos y lectura a base de datos no relacionales

#### 5.Next.js

Es un marco web de desarrollo front-end de React de código abierto, con funcionalidades como la representación del lado del servidor y la generación de sitios web estáticos para aplicaciones web basadas en React. Al ser un lenguaje liviano es eficiente para el logeo, carga y consulta de datos.frw 

### Flujo de datos

****************Imagen *********************

#### 1. Consulta por ID

Consultar datos transaccionales por ID desde una aplicación frontend o servicio backend desarrollado en Next.js, utilizando MongoDB como base de datos. 

#### 2. Flujo de autenticación

Implica la verificación de credenciales de usuario utilizando Redis como almacén de caché para información de autenticación. Se busca el usuario o correo electrónico en Redis para validar la autenticidad del usuario. 

#### 3. Flujo de analítica

Análisis a partir de visualizaciones utilizando herramientas de Business Intelligence, las cuales realizan consultas a base de datos SQL.

#### 4. Carga de datos

- Carga Data Transaccional a MongoDB: 

Involucra la carga de datos transaccionales desde una aplicación frontend o interfaz de consola utilizando Python, y cargando los datos en MongoDB. 

- Carga Data Transaccional a SQL: 

Implica la carga de datos transaccionales desde una aplicación frontend o interfaz de consola utilizando Python, y cargando los datos en una base de datos SQL. 

- Carga Analítica a MongoDB y SQL: 

Consiste en la carga de datos desde un servicio Python, primero a MongoDB para almacenamiento temporal y luego a una base de datos SQL para un análisis.

### Tecnologías utilizadas

La arquitectura se fundamenta en Docker Compose para garantizar la escabilidad del proceso. Desde la perspectiva del backend, se contemplan tres motores de base de datos, los cuales son Redis, Mongo DB y SQL. Cada motor procesa la información con base en información transaccional o proceso de analítica. Así mismo, se utilizará el lenguaje de programación python para el pre-procesamiento de información.  

Desde la perspectiva frontend, se desplegará la herramienta mediante Next.js y de ser necesario, una herramienta de visualización (dashboard) para el proceso de analítica. 

### Lenguajes de programación y frameworks

Se optó por usar los siguientes lenguajes de programación: 

Python, JavaScript, Node.js, SQL, NoSQL y framework Next.js, el cual fundamenta su trabajo en javascript, en su versión 14 

### Configuración e instalación

### Uso del proyecto

### Mantenimiento y soporte

### Contribuciones

### Licencia

### Agradecimientos

### Descripción de cada archivo y directorio

**** Imagen de la estructura del repositorio







