# RtG-Language

Lenguaje de alto nivel para describir estructuras y proyectos basados en **RtG-Format**.

> **Estado:** Diseño definido / implementación pendiente  
> **Versión del lenguaje:** `2.0`

---

# 1. Propósito

**RtG-Language** es un lenguaje fuente diseñado para permitir escribir estructuras de RtG-Format de forma legible, organizada y mantenible.

Un archivo:

```text
.rtg
```

contiene código fuente de RtG-Language.

El compilador transforma ese código en el formato nativo de RtG-Format:

```text
.rtg
  ↓
Lexer
  ↓
Parser
  ↓
AST
  ↓
Resolver
  ↓
Compiler
  ↓
RtG-Format
```

RtG-Language **no reemplaza RtG-Format**.

RtG-Format continúa siendo el formato de salida y la especificación estructural fundamental.

---

# 2. Objetivos

RtG-Language debe:

- ser legible por humanos;
- representar estructuras complejas sin editar manualmente índices internos;
- permitir múltiples instancias del mismo tipo;
- permitir conexiones entre instancias;
- permitir conexiones entre diferentes secciones;
- permitir propiedades globales y específicas;
- permitir attachments mediante UUID;
- utilizar metadata externa mediante schemas;
- validar referencias antes de generar el resultado;
- producir RtG-Format válido;
- mantener una sintaxis formal y única;
- evitar sintaxis ambiguas o redundantes.

---

# 3. Principio fundamental

RtG-Language es una **representación fuente**.

El usuario escribe:

```rtg
instance "Wheel" as frontLeft;
```

y:

```rtg
connect frontLeft -> chassis {
    localType: 1;
    point: 1;
}
```

El compilador se encarga de resolver los identificadores y generar la representación interna que necesita RtG-Format.

El usuario **no controla directamente los índices internos del formato de salida**.

---

# 4. Compatibilidad con RtG-Format

El formato nativo de RtG-Format utiliza conceptualmente:

```text
[TipoDelBloque, Conexiones, Propiedades]
```

Las conexiones utilizan:

```text
[TipoLocal, PuntoPadre/UUID, IndicePadre]
```

Los índices son **1-based**.

RtG-Language no debe cambiar estas reglas.

En particular:

```text
IndicePadre
```

es un dato interno del compilador.

No es responsabilidad del usuario escribirlo manualmente.

---

# 5. Archivo mínimo

Un archivo puede comenzar con:

```rtg
rtg 2.0;
```

La declaración de versión identifica la versión de la sintaxis utilizada por el archivo.

---

# 6. Schema

Un archivo puede declarar un schema:

```rtg
schema {
    source: "./schema.json";
}
```

El schema proporciona metadata que el compilador puede utilizar para validar y resolver información de RtG-Format.

Puede proporcionar, entre otras cosas:

- tipos de bloques;
- `TipoLocal`;
- puntos de conexión;
- metadata de conexiones;
- información necesaria para validación.

El schema **no redefine arbitrariamente RtG-Format**.

---

# 7. Objetos

Las estructuras lógicas se agrupan mediante:

```rtg
object "CarBody" {
    ...
}
```

El nombre del objeto es organizativo.

Los objetos no son necesariamente archivos separados ni builds independientes.

Un mismo archivo puede contener varios objetos:

```rtg
object "CarBody" {
    ...
}

object "Seats" {
    ...
}
```

---

# 8. Secciones lógicas

Los `object` son **secciones lógicas dentro del mismo proyecto/archivo**.

No deben interpretarse como builds independientes.

Por ejemplo:

```rtg
object "CarBody" {
    instance "Chassis" as chassis;
}

object "Seats" {
    instance "Seat" as driverSeat;
}
```

`driverSeat` puede conectarse con `chassis`.

Las secciones no crean límites de referencia.

---

# 9. Instancias

Una instancia se declara mediante:

```rtg
instance "Tipo" as identificador;
```

Ejemplo:

```rtg
instance "Chassis" as chassis;
instance "Wheel" as frontLeft;
instance "Wheel" as frontRight;
```

El primer valor es el tipo de bloque RtG-Format.

El identificador después de `as` es una referencia del lenguaje.

---

# 10. Identificadores

Los identificadores son referencias reales del compilador.

Ejemplo:

```rtg
instance "Wheel" as frontLeft;
```

Después:

```rtg
connect frontLeft -> chassis {
    localType: 1;
    point: 1;
}
```

El compilador debe resolver:

```text
frontLeft
    ↓
instancia correspondiente
    ↓
índice interno RtG-Format
```

Los identificadores deben ser únicos dentro del ámbito definido por el lenguaje.

No deben utilizarse referencias compactas ni índices escritos manualmente.

---

# 11. Múltiples instancias del mismo tipo

Está permitido crear múltiples instancias del mismo tipo:

```rtg
instance "Wheel" as frontLeft;
instance "Wheel" as frontRight;
instance "Wheel" as rearLeft;
instance "Wheel" as rearRight;
```

Cada instancia tiene su propio identificador.

Esto permite diferenciar instancias del mismo tipo sin introducir nombres artificiales dentro del tipo RtG-Format.

---

# 12. Propiedades

Las propiedades se escriben mediante:

```rtg
properties {
    "RGB": [255, 0, 0];
    "Visible": true;
}
```

Las propiedades utilizan claves explícitas.

No existe una lista cerrada de propiedades impuesta por RtG-Language.

El compilador debe preservar las propiedades válidas según las reglas de RtG-Format.

---

# 13. Propiedades de instancia

Una instancia puede tener sus propias propiedades:

```rtg
instance "Seat" as passengerSeat {
    properties {
        "RGB": [0, 0, 255];
    }
}
```

Esto permite modificar únicamente esa instancia.

---

# 14. Propiedades globales

Un `object` puede definir propiedades globales:

```rtg
object "Seats" {
    properties {
        "RGB": [255, 0, 0];
    }

    instance "Seat" as driverSeat;
    instance "Seat" as passengerSeat;
}
```

Las propiedades globales se aplican a las instancias correspondientes dentro de esa sección.

---

# 15. Precedencia de propiedades

Las propiedades específicas de una instancia tienen prioridad sobre las propiedades globales cuando utilizan la misma clave.

Ejemplo:

```rtg
object "Seats" {
    properties {
        "RGB": [255, 0, 0];
    }

    instance "Seat" as driverSeat;

    instance "Seat" as passengerSeat {
        properties {
            "RGB": [0, 0, 255];
        }
    }
}
```

Resultado conceptual:

```text
driverSeat
    RGB = [255, 0, 0]

passengerSeat
    RGB = [0, 0, 255]
```

La regla es:

```text
instance properties
        ↓
override
        ↓
global properties
```

La sobreescritura solamente afecta a claves con el mismo nombre.

---

# 16. Conexiones

Las conexiones utilizan:

```rtg
connect child -> parent {
    localType: 1;
    point: 1;
}
```

La instancia situada a la izquierda es el objeto que se conecta.

La instancia situada a la derecha es el padre.

Ejemplo:

```rtg
connect frontLeft -> chassis {
    localType: 1;
    point: 1;
}
```

---

# 17. `localType`

Cada conexión declara explícitamente:

```rtg
localType: 1;
```

El valor debe corresponder a un `TipoLocal` válido según la metadata utilizada por el compilador/schema.

RtG-Language no debe inventar valores.

El compilador debe validar el valor antes de generar RtG-Format.

---

# 18. Punto de conexión

El punto de conexión se declara mediante:

```rtg
point: 13;
```

Los puntos numéricos utilizan la información correspondiente de RtG-Format/schema.

El lenguaje también permite utilizar UUID:

```rtg
point: uuid("{...}");
```

---

# 19. Conexiones mediante UUID

Cuando una conexión necesita utilizar un attachment identificado por UUID:

```rtg
connect child -> parent {
    localType: 1;
    point: uuid("{...}");
}
```

El compilador debe validar que el UUID sea válido y resolverlo según las reglas de RtG-Format.

---

# 20. Attachments

Los attachments pueden declararse mediante:

```rtg
attachment "{UUID}" on chassis {
    partName: "Chassis";
    cframe: [
        1, 0, 0,
        0, 1, 0,
        0, 0, 1,
        0, 0, 0
    ];
}
```

El attachment identifica:

```text
UUID
Part name
CFrame
Parent instance
```

---

# 21. EphemeralAttachments

Los attachments corresponden a la información necesaria para generar la estructura `EphemeralAttachments` de RtG-Format.

Conceptualmente:

```text
EphemeralAttachments
└── UUID
    ├── partName
    └── cframe
```

El `cframe` debe contener exactamente los valores requeridos por RtG-Format:

```text
[x, y, z, r1, r2, r3, r4, r5, r6, r7, r8, r9]
```

Es decir:

```text
3 valores de posición
+
9 valores de rotación
=
12 valores
```

El compilador debe validar la cantidad de valores.

---

# 22. CFrame

Un CFrame de attachment debe contener exactamente 12 números:

```rtg
cframe: [
    x, y, z,
    r1, r2, r3,
    r4, r5, r6,
    r7, r8, r9
];
```

Una cantidad incorrecta debe producir un error de compilación.

---

# 23. Referencias entre objetos

Las instancias pueden estar declaradas en diferentes objetos lógicos.

Ejemplo:

```rtg
object "CarBody" {
    instance "Chassis" as chassis;
}

object "Wheels" {
    instance "Wheel" as frontLeft;

    connect frontLeft -> chassis {
        localType: 1;
        point: 1;
    }
}
```

Esto es válido siempre que ambas referencias puedan resolverse.

Los objetos no deben convertirse en scopes aislados que impidan conexiones válidas entre secciones.

---

# 24. Resolución

El compilador debe realizar una fase de resolución después del parsing.

Conceptualmente:

```text
Source
  ↓
Lexer
  ↓
Parser
  ↓
AST
  ↓
Resolver
  ├── Identifier Resolver
  ├── Schema Resolver
  ├── Connection Resolver
  ├── Property Resolver
  └── Attachment Resolver
  ↓
Compiler
  ↓
RtG-Format
```

---

# 25. Estado interno del compilador

El compilador puede mantener estructuras internas equivalentes a:

```text
instances
objects
connections
properties
global_properties
attachments
uuids
schema
resolved_indexes
```

Estas estructuras son internas.

No forman parte de la sintaxis pública de RtG-Language.

---

# 26. Índices internos

RtG-Language no debe permitir:

```rtg
parentIndex: 4;
```

ni mecanismos equivalentes.

El compilador determina automáticamente los índices internos necesarios.

Por ejemplo:

```rtg
instance "Chassis" as chassis;
instance "Wheel" as frontLeft;
```

El compilador decide qué índices corresponden a esas instancias en la salida.

Esto permite reorganizar el código fuente sin obligar al usuario a recalcular índices manualmente.

---

# 27. Output

El archivo puede declarar el destino:

```rtg
output {
    file: "./car.json";
}
```

El compilador debe producir el archivo de salida correspondiente.

La ruta de salida forma parte de la configuración del archivo fuente cuando se utiliza esta declaración.

---

# 28. Ejemplo completo

```rtg
rtg 2.0;

schema {
    source: "./schema.json";
}

object "CarBody" {
    instance "Chassis" as chassis;
    instance "Wheel" as frontLeft;

    connect frontLeft -> chassis {
        localType: 1;
        point: 1;
    }
}

object "Seats" {
    properties {
        "RGB": [255, 0, 0];
        "Visible": true;
    }

    instance "Seat" as driverSeat;

    instance "Seat" as passengerSeat {
        properties {
            "RGB": [0, 0, 255];
        }
    }

    connect driverSeat -> chassis {
        localType: 1;
        point: 13;
    }
}

output {
    file: "./car.json";
}
```

Este ejemplo demuestra:

- versión;
- schema;
- objetos;
- instancias;
- identificadores;
- múltiples instancias;
- propiedades globales;
- propiedades específicas;
- override de propiedades;
- conexiones;
- `localType`;
- puntos de conexión;
- conexiones entre objetos;
- output.

---

# 29. Gramática formal

La gramática base definida para RtG-Language 2.0 es:

```text
file = header, schema?, object*, output?;

header = "rtg", version, ";";

schema =
    "schema", "{",
        "source", ":", string, ";",
    "}";

object =
    "object", string, "{",
        property_block?,
        attachment*,
        instance*,
        connection*,
    "}";

instance =
    "instance", string,
    "as", identifier,
    property_block?,
    ";";

connection =
    "connect", identifier,
    "->", identifier,
    "{",
        "localType", ":", integer, ";",
        "point", ":", point_reference,
    "}";

point_reference =
    integer
    |
    "uuid", "(", uuid, ")";

property_block =
    "properties", "{",
        json_member*,
    "}";

attachment =
    "attachment", uuid,
    "on", identifier,
    "{",
        "partName", ":", string, ";",
        "cframe", ":", number_array,
    "}";

output =
    "output", "{",
        "file", ":", string, ";",
    "}";
```

Esta gramática representa la sintaxis definida actualmente.

No se deben introducir aliases informales sin modificar primero la especificación.

---

# 30. Sintaxis eliminada

RtG-Language 2.0 no utiliza construcciones históricas como:

```text
track
create
note-names
Order
```

Tampoco utiliza:

```text
[Type:N]
```

como mecanismo de referencia.

Las referencias deben utilizar identificadores:

```rtg
instance "Wheel" as frontLeft;
```

y:

```rtg
connect frontLeft -> chassis {
    ...
}
```

Tampoco se permite controlar manualmente los índices internos de RtG-Format.

---

# 31. Sintaxis formal

El lenguaje debe tener una única forma oficial de expresar cada concepto.

No deben existir múltiples formas equivalentes como:

```text
forma A
forma B
forma abreviada
forma legacy
```

para realizar la misma operación.

Esto permite:

- documentación consistente;
- parser más sencillo;
- mejores diagnósticos;
- tooling más predecible;
- menor ambigüedad.

---

# 32. Validación

El compilador debe validar el programa antes de generar el resultado.

Como mínimo debe detectar:

```text
Unknown identifier
Duplicate identifier
Unknown parent
Unknown connection point
Invalid TipoLocal
Invalid UUID
Invalid CFrame length
Invalid property syntax
Invalid schema
Invalid output
Syntax errors
```

Los errores deben proporcionar información suficiente para localizar el problema en el archivo fuente.

---

# 33. AST

El parser debe producir un **AST (Abstract Syntax Tree)**.

El AST representa la estructura semántica del programa.

No debe utilizarse como una simple copia textual del archivo.

Conceptualmente:

```text
File
├── Header
├── Schema
├── Objects
│   ├── Properties
│   ├── Attachments
│   ├── Instances
│   └── Connections
└── Output
```

---

# 34. Compiler

El compilador transforma el AST resuelto en RtG-Format.

El proceso conceptual es:

```text
.rtg
 ↓
Lexer
 ↓
Tokens
 ↓
Parser
 ↓
AST
 ↓
Resolver
 ↓
Validated AST
 ↓
Compiler
 ↓
RtG-Format
```

El compilador debe encargarse de:

- ordenar/resolver instancias según sea necesario;
- generar índices internos;
- resolver padres;
- resolver UUID;
- aplicar propiedades globales;
- aplicar overrides;
- generar conexiones;
- generar attachments;
- producir la estructura final RtG-Format.

---

# 35. Cache

RtG-Language utilizará un único archivo de cache por proyecto:

```text
.rtgcache
```

No debe ser una carpeta.

Ejemplo:

```text
MyProject/
├── schema.json
├── car.rtg
├── house.rtg
├── car.json
├── house.json
└── .rtgcache
```

---

# 36. Contenido de `.rtgcache`

El cache puede contener información como:

```text
Cache metadata
Compiler version
Cache format version
Source hashes
Schema hash
Parsed ASTs
Processed schema
Resolved identifiers
Resolved connections
Resolved properties
Resolved attachments
Reusable build results
```

El objetivo es evitar trabajo repetido cuando los archivos relevantes no han cambiado.

---

# 37. Propiedades del cache

`.rtgcache` debe ser:

- regenerable;
- opcional;
- seguro de eliminar;
- independiente del código fuente;
- invalidable cuando cambie el compilador;
- invalidable cuando cambie el schema;
- invalidable cuando cambien los archivos fuente.

**Eliminar `.rtgcache` nunca debe romper el proyecto.**

El compilador debe poder reconstruirlo desde cero.

El formato interno puede ser binario si resulta conveniente.

Los usuarios no necesitan editar `.rtgcache` manualmente.

---

# 38. Invalidación del cache

El cache debe invalidarse cuando cambie información relevante.

Como mínimo debe considerarse:

```text
.rtg source hash
schema hash
compiler version
cache format version
```

Por ejemplo:

```text
car.rtg
   ↓
hash cambiado
   ↓
reparse/recompile
```

Mientras que:

```text
car.rtg
   ↓
hash sin cambios
schema sin cambios
compiler compatible
   ↓
cache reutilizable
```

---

# 39. Proyecto

Un proyecto puede contener múltiples archivos `.rtg`.

Ejemplo:

```text
MyProject/
├── schema.json
├── car.rtg
├── house.rtg
├── car.json
├── house.json
└── .rtgcache
```

El cache es compartido por el proyecto.

No debe existir un `.rtgcache` independiente por cada `.rtg` salvo que una futura especificación lo defina explícitamente.

---

# 40. VS Code

RtG-Language está destinado a disponer de una extensión para Visual Studio Code.

La extensión debe manejar principalmente:

```text
.rtg
```

y proporcionar:

- identificación del lenguaje;
- syntax highlighting;
- configuración del lenguaje;
- snippets;
- icono del archivo;
- asociación `.rtg`.

La extensión de VS Code y el compilador son componentes conceptualmente separados.

---

# 41. Extensión VS Code

La extensión puede tener una estructura similar a:

```text
extension/
├── language-configuration.json
├── syntaxes/
│   └── rtg-language.tmLanguage.json
├── snippets/
│   └── rtg-language.json
└── icons/
    └── rtg-file.svg
```

Posteriormente puede empaquetarse como:

```text
.vsix
```

para instalarla en VS Code.

---

# 42. Compilador

El compilador puede implementarse como un paquete independiente.

Una estructura prevista es:

```text
rtg_language/
├── lexer/
├── parser/
├── resolver/
├── schema/
├── compiler/
├── cache/
└── diagnostics/
```

La CLI puede proporcionar posteriormente una interfaz como:

```text
rtg build car.rtg
```

pero la sintaxis final del comando corresponde al contrato de RtG-CLI.

---

# 43. Relación con RtG-CLI

La arquitectura prevista es:

```text
RtG-CLI
    │
    └── RtG-Language compiler
            │
            ├── Lexer
            ├── Parser
            ├── Resolver
            ├── Schema
            ├── Cache
            └── Compiler
                    │
                    ▼
                RtG-Format
```

RtG-Language no debe depender de comportamientos ambiguos o no documentados de RtG-CLI.

Primero debe existir un contrato claro entre ambos proyectos.

---

# 44. Estructura prevista del proyecto

Una estructura inicial puede ser:

```text
RtG-Language/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── package.json
├── pyproject.toml
│
├── extension/
│   ├── language-configuration.json
│   ├── syntaxes/
│   │   └── rtg-language.tmLanguage.json
│   ├── snippets/
│   │   └── rtg-language.json
│   └── icons/
│       └── rtg-file.svg
│
├── cli/
│   ├── __init__.py
│   └── main.py
│
├── rtg_language/
│   ├── __init__.py
│   ├── lexer/
│   ├── parser/
│   ├── resolver/
│   ├── schema/
│   ├── compiler/
│   ├── cache/
│   └── diagnostics/
│
├── schema/
│   ├── schema.json
│   └── README.md
│
├── examples/
│   ├── basic.rtg
│   ├── connections.rtg
│   ├── properties.rtg
│   ├── attachments.rtg
│   └── complete.rtg
│
├── tests/
│   ├── lexer/
│   ├── parser/
│   ├── resolver/
│   ├── schema/
│   ├── compiler/
│   └── cache/
│
└── docs/
    ├── LANGUAGE.md
    ├── SYNTAX.md
    ├── GRAMMAR.md
    ├── COMPILER.md
    ├── CACHE.md
    └── VS-CODE.md
```

Esta estructura es una propuesta inicial y puede cambiar si la implementación demuestra que otra organización es técnicamente superior.

---

# 45. Tests

RtG-Language debe contar con pruebas automatizadas.

Deben cubrir al menos:

```text
Lexer
Parser
AST
Identifiers
Instances
Connections
Schema
Properties
Global properties
Property overrides
UUID
Attachments
CFrame
Cross-object references
Output
Validation
Compiler
Cache
```

También deben existir casos inválidos.

---

# 46. Ejemplos de errores

Un identificador inexistente:

```rtg
connect wheel -> chassis {
    localType: 1;
    point: 1;
}
```

debe producir un diagnóstico si `wheel` no fue declarado.

Un CFrame incorrecto:

```rtg
cframe: [1, 2, 3];
```

debe producir un error porque no contiene los 12 valores requeridos.

Un `localType` inválido debe detectarse mediante la información del schema correspondiente.

---

# 47. No inventar schema

El compilador no debe inventar:

```text
TipoLocal
puntos
bloques
propiedades
conexiones
```

cuando esa información no esté definida.

Si el compilador necesita metadata para validar algo, debe obtenerla del schema o de la especificación real de RtG-Format.

---

# 48. No mezclar RtG-Preview

RtG-Preview pertenece a una etapa anterior/beta del ecosistema y es considerado obsoleto para el trabajo actual relacionado con RtG-Language y PolaroidPhoto.

Por tanto:

```text
RtG-Language
    ≠
RtG-Preview
```

La implementación actual no debe depender de RtG-Preview.

---

# 49. PolaroidPhoto

RtG-Language debe poder representar propiedades reales de RtG-Format sin inventar nombres.

Por ejemplo, cuando corresponda a la especificación actual:

```text
Phrase
```

debe utilizarse el nombre real definido por el formato, no una variante histórica como:

```text
Caption
```

La regla general es siempre utilizar los nombres reales definidos por RtG-Format.

---

# 50. Diseño definitivo de sintaxis

La sintaxis oficial de RtG-Language 2.0 se basa en:

```rtg
rtg 2.0;

schema {
    source: "./schema.json";
}

object "Name" {
    properties {
        "Property": value;
    }

    instance "Type" as identifier;

    connect identifier -> parent {
        localType: 1;
        point: 1;
    }
}

output {
    file: "./output.json";
}
```

No deben añadirse formas abreviadas sin una modificación explícita de la especificación.

---

# 51. Filosofía del lenguaje

RtG-Language debe priorizar:

```text
Claridad
    ↓
Corrección
    ↓
Validación
    ↓
Mantenibilidad
    ↓
Extensibilidad
```

sobre:

```text
Sintaxis extremadamente corta
```

La intención es que un archivo `.rtg` pueda entenderse leyendo el código fuente sin tener que conocer índices internos de RtG-Format.

---

# 52. Regla de oro

El código fuente debe describir **qué estructura se quiere construir**.

El compilador debe encargarse de **cómo representarla internamente en RtG-Format**.

Por ejemplo, el usuario escribe:

```rtg
connect frontLeft -> chassis {
    localType: 1;
    point: 1;
}
```

y no:

```text
conexión = [1, 2, 1]
```

porque los detalles internos de serialización pertenecen al compilador.

---

# 53. Estado del proyecto

Actualmente:

```text
Sintaxis 2.0             DEFINIDA
Gramática                 DEFINIDA
Modelo conceptual         DEFINIDO
Conexiones                DEFINIDAS
Propiedades               DEFINIDAS
Attachments               DEFINIDOS
Cache                     DISEÑADO
VS Code extension         PLANIFICADA
Compiler                  PENDIENTE
Tests                     PENDIENTES
Implementación            PENDIENTE
```

---

# 54. Orden recomendado de implementación

La implementación debe realizarse en este orden:

```text
1. Lexer
       ↓
2. Parser
       ↓
3. AST
       ↓
4. Diagnostics
       ↓
5. Schema loader
       ↓
6. Identifier resolver
       ↓
7. Connection resolver
       ↓
8. Property resolver
       ↓
9. Attachment resolver
       ↓
10. Compiler
       ↓
11. Cache
       ↓
12. CLI integration
       ↓
13. VS Code extension
       ↓
14. Tests completos
       ↓
15. Documentation
```

Cada fase debe probarse antes de construir dependencias sobre ella.

---

# 55. Criterio de finalización

RtG-Language se considera funcional cuando pueda:

1. leer un archivo `.rtg`;
2. tokenizarlo;
3. construir su AST;
4. validar su sintaxis;
5. cargar el schema;
6. resolver identificadores;
7. resolver conexiones;
8. resolver propiedades;
9. resolver attachments;
10. validar UUID;
11. validar CFrame;
12. generar índices internos automáticamente;
13. producir RtG-Format válido;
14. generar el archivo especificado mediante `output`;
15. reutilizar `.rtgcache` cuando sea válido;
16. reconstruir el cache cuando sea necesario;
17. funcionar sin `.rtgcache`;
18. producir diagnósticos útiles;
19. disponer de tests automatizados;
20. poder integrarse con RtG-CLI sin depender de APIs informales.

---

# 56. Principio final

**RtG-Language es una capa de lenguaje sobre RtG-Format, no una modificación de RtG-Format.**

La separación debe mantenerse:

```text
RtG-Language
    │
    │ fuente legible
    ▼
Compiler
    │
    │ representación nativa
    ▼
RtG-Format
```

El lenguaje debe hacer que escribir RtG-Format sea más fácil, sin alterar las reglas fundamentales del formato.