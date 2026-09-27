# RtG-CLI

CLI oficial del ecosistema **RtG-Format**.

> **Estado:** En reconstrucción / rediseño  
> **Objetivo:** Establecer una base formal, extensible y estable para las herramientas de RtG-Format y su futura integración con RtG-Language.

---

## 1. Propósito

**RtG-CLI** es la interfaz de línea de comandos del ecosistema RtG-Format.

Su función es proporcionar una interfaz común para:

- consultar información de RtG-Format;
- mostrar ayuda y reglas;
- administrar idiomas;
- descubrir y ejecutar addons;
- ejecutar comandos auxiliares del ecosistema;
- gestionar versiones;
- proporcionar una base estable para herramientas futuras;
- servir como punto de integración para **RtG-Language**.

RtG-CLI debe ser una herramienta formal y mantenible, no un conjunto de comandos implementados de manera independiente.

---

# 2. Principios fundamentales

El desarrollo de RtG-CLI debe seguir estos principios.

### 2.1 No inventar RtG-Format

RtG-CLI debe respetar la especificación real de RtG-Format.

No se deben inventar:

- tipos de bloques;
- propiedades;
- conexiones;
- índices;
- estructuras JSON;
- reglas de serialización;
- comportamientos del formato.

Si algo no está definido por RtG-Format, debe investigarse en el repositorio o documentarse como una decisión nueva antes de implementarlo.

---

### 2.2 Separación de responsabilidades

RtG-CLI debe separar claramente:

```text
CLI
├── Argument parsing
├── Command dispatch
├── Configuration
├── Language management
├── Addon management
├── Program command execution
├── Diagnostics / errors
├── Version information
└── Help / rules
```

Cada componente debe tener una responsabilidad clara.

La lógica de los addons no debe estar mezclada con el parser principal de argumentos.

---

### 2.3 Extensibilidad

RtG-CLI debe permitir añadir nuevos comandos y addons sin modificar innecesariamente el núcleo.

La arquitectura debe permitir que en el futuro existan herramientas como:

```text
rtg build
rtg validate
rtg format
rtg inspect
rtg addon ...
```

sin tener que reconstruir toda la CLI.

---

# 3. Relación con RtG-Format

RtG-CLI forma parte del ecosistema:

```text
RtG ecosystem
│
├── RtG-Format
│   └── Formato de datos
│
├── RtG-CLI
│   └── Interfaz de comandos
│
├── RtG-Language
│   └── Lenguaje fuente
│       └── .rtg → RtG-Format
│
└── Otros proyectos
    ├── herramientas
    ├── addons
    └── utilidades
```

RtG-CLI **no reemplaza RtG-Format**.

RtG-Format continúa siendo la especificación del formato de datos.

---

# 4. Futura integración con RtG-Language

RtG-Language será un lenguaje fuente para producir archivos RtG-Format.

La arquitectura prevista es:

```text
archivo.rtg
     │
     ▼
   Lexer
     │
     ▼
   Parser
     │
     ▼
    AST
     │
     ▼
  Resolver
     │
     ├── Schema Resolver
     ├── Connection Resolver
     ├── Property Resolver
     └── Attachment Resolver
     │
     ▼
  Compiler
     │
     ▼
RtG-Format JSON
```

RtG-CLI debe proporcionar una interfaz estable para que posteriormente pueda existir algo como:

```text
rtg build car.rtg
```

o una interfaz equivalente definida durante la reconstrucción.

La sintaxis exacta del comando debe decidirse formalmente durante el trabajo de RtG-CLI.

**No se debe implementar una interfaz provisional que luego entre en conflicto con RtG-Language.**

---

# 5. RtG-Language: contrato conocido

La futura integración debe respetar las decisiones ya establecidas para RtG-Language.

Ejemplo:

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

output {
    file: "./car.json";
}
```

Las referencias internas son identificadores reales:

```rtg
instance "Chassis" as chassis;
```

Las conexiones utilizan esos identificadores:

```rtg
connect frontLeft -> chassis {
    localType: 1;
    point: 1;
}
```

Los índices internos del RtG-Format son responsabilidad del compilador.

El usuario de RtG-Language **no debe controlar manualmente esos índices**.

---

# 6. Schema

RtG-Language podrá utilizar información externa del schema:

```rtg
schema {
    source: "./schema.json";
}
```

El schema puede proporcionar metadata necesaria para:

- tipos locales;
- puntos de conexión;
- información de bloques;
- validación;
- resolución de conexiones.

El schema es metadata del lenguaje/compilador.

No debe modificar arbitrariamente la estructura nativa de RtG-Format.

---

# 7. Propiedades

Las propiedades de RtG-Language deben permanecer abiertas.

Ejemplo:

```rtg
properties {
    "RGB": [255, 0, 0];
    "Visible": true;
}
```

No debe crearse una lista cerrada de propiedades inventada por RtG-CLI.

Las propiedades deben terminar representándose según las reglas reales de RtG-Format.

---

# 8. Conexiones

El formato nativo conocido utiliza:

```text
[TipoLocal, PuntoPadre/UUID, IndicePadre]
```

Los índices son internos y comienzan en 1.

RtG-Language utiliza una forma más legible:

```rtg
connect child -> parent {
    localType: 1;
    point: 13;
}
```

También puede utilizar UUID:

```rtg
connect child -> parent {
    localType: 1;
    point: uuid("{...}");
}
```

RtG-CLI y sus futuras herramientas no deben introducir otra representación incompatible.

---

# 9. Addons

RtG-CLI actualmente posee un concepto de **addons**.

Los addons deben convertirse en un sistema formal.

Conceptualmente:

```text
RtG-CLI
   │
   ├── Core commands
   │
   └── Addons
       ├── addon A
       ├── addon B
       └── addon C
```

Cada addon debe tener:

- identificador interno estable;
- nombre;
- descripción;
- versión cuando corresponda;
- comandos disponibles;
- argumentos;
- documentación;
- mecanismo de ejecución;
- código de salida;
- manejo de errores.

El identificador interno del addon puede ser distinto de su nombre descriptivo.

Por ejemplo:

```text
ID: image
Name: Image Tools
```

Los identificadores internos deben mantenerse estables siempre que sea posible.

---

# 10. Ejecución real de addons

Un problema que debe resolverse durante la reconstrucción es la diferencia entre:

```text
descubrir un addon
```

y

```text
ejecutar un addon
```

Mostrar información de un addon no constituye su ejecución.

El sistema final debe definir claramente:

```text
Arguments
    ↓
Addon
    ↓
Execution
    ├── stdout
    ├── stderr
    ├── exit code
    └── errors
```

Debe quedar documentado:

- cómo se pasan argumentos;
- cómo se recibe stdin, si existe;
- cómo se produce stdout;
- cómo se produce stderr;
- qué representa el código de salida;
- cómo se manejan errores;
- cómo se cancela una ejecución;
- cómo se ejecutan programas externos;
- cómo se ejecutan programas escritos en Python, JavaScript u otros lenguajes si el sistema los admite.

No debe quedar una API implícita.

---

# 11. Program Commands

RtG-CLI contiene el concepto de **program commands**.

Este concepto debe formalizarse.

Debe definirse:

```text
Program Command
├── ID
├── Name
├── Description
├── Arguments
├── Input
├── Execution method
├── Output
├── Error output
├── Exit code
└── Environment / configuration
```

La documentación debe explicar exactamente qué significa un `program command`.

No debe depender de comportamiento accidental del código actual.

---

# 12. Parsing de argumentos

El sistema actual de argumentos contiene decisiones históricas relacionadas con:

```text
-
--
```

y diferentes formas de comandos y opciones.

Durante la reconstrucción se debe revisar completamente este sistema.

El objetivo es evitar ambigüedades como:

```text
RtG-CLI option
vs.
addon option
vs.
program argument
```

La nueva arquitectura debe definir formalmente:

1. cómo se identifica un comando;
2. cómo se identifican subcomandos;
3. cómo se identifican opciones;
4. cómo se pasan argumentos posicionales;
5. cómo se pasan opciones a addons;
6. cómo se separan argumentos del CLI de argumentos de un programa externo.

Ejemplo conceptual:

```text
rtg <command> [options] [arguments]
```

La sintaxis final debe definirse durante la reconstrucción.

---

# 13. Comandos principales

Los comandos existentes deben auditarse antes de conservarlos.

Entre las capacidades existentes/históricas se encuentran:

```text
help
version
rules
language
commands
addons
```

También existen addons como:

```text
image
preview
```

Esto no significa que todos deban conservar exactamente la misma interfaz.

Cada comando debe ser:

- documentado;
- probado;
- consistente;
- compatible con el sistema de argumentos;
- integrado en el dispatcher.

---

# 14. Languages

RtG-CLI tiene un sistema relacionado con idiomas.

Actualmente existen varias formas históricas de solicitar el idioma, por ejemplo:

```text
-language
-lang
--lang
```

Este sistema debe revisarse.

Debe definirse formalmente:

- opción oficial;
- aliases permitidos;
- idioma predeterminado;
- detección automática, si existe;
- comportamiento ante idiomas inexistentes;
- ubicación de las traducciones;
- formato de los archivos de idioma;
- prioridad entre configuración, argumentos y detección automática.

La arquitectura debe permitir añadir idiomas sin modificar manualmente toda la CLI.

---

# 15. `assets.json`

El proyecto ha utilizado un archivo `assets.json` que contiene diferentes tipos de información.

Históricamente puede incluir elementos como:

- información de CLI;
- idiomas;
- ayuda;
- reglas;
- addons;
- metadata de addons;
- program commands;
- versiones.

Durante la reconstrucción debe determinarse si esta estructura:

1. debe mantenerse;
2. debe dividirse;
3. debe formalizarse mediante un schema;
4. debe reemplazarse por otra arquitectura.

No se debe cambiar simplemente por estética.

Debe analizarse qué información consume realmente cada componente.

---

# 16. Versionado

La información de versión debe tener una única fuente de verdad o una estrategia formal de sincronización.

Deben revisarse campos históricos como:

```text
version
version-date
version-content
```

Debe definirse:

- versión de RtG-CLI;
- versión de RtG-Format cuando corresponda;
- versión de addons;
- compatibilidad;
- formato de salida de `--version`.

No deben existir versiones contradictorias en distintos archivos.

---

# 17. Help

La ayuda debe formar parte de la arquitectura.

Debe poder explicar:

```text
rtg --help
```

y comandos específicos:

```text
rtg <command> --help
```

La ayuda debe generarse a partir de metadata formal cuando sea posible.

No debería ser necesario mantener manualmente grandes bloques de texto duplicados en diferentes partes del código.

---

# 18. Rules

RtG-CLI puede proporcionar acceso a las reglas de RtG-Format.

Estas reglas deben proceder de la documentación/especificación real.

No deben duplicarse reglas inventadas dentro del código de la CLI.

---

# 19. Preview

El addon histórico:

```text
preview
```

debe auditarse cuidadosamente.

El antiguo **RtG-Preview** corresponde a una etapa beta/obsoleta del proyecto y no debe asumirse como parte de la arquitectura moderna de RtG.

Durante la reconstrucción debe determinarse formalmente si el addon:

- continúa como legacy;
- queda deprecated;
- se elimina del registro activo;
- se conserva únicamente por compatibilidad.

La decisión debe basarse en el estado real del repositorio y documentarse.

No se debe integrar RtG-Preview antiguo dentro de RtG-Language moderno.

---

# 20. Compatibilidad con RtG-Format

La reconstrucción de RtG-CLI debe evitar cambios involuntarios en:

- JSON generado;
- estructura de bloques;
- conexiones;
- propiedades;
- UUID;
- EphemeralAttachments;
- CFrame;
- índices;
- nombres definidos por el formato.

Una herramienta de CLI no debe reinterpretar el formato.

---

# 21. Arquitectura objetivo

Una arquitectura conceptual recomendada es:

```text
rtg_cli/
│
├── cli/
│   ├── parser
│   ├── dispatcher
│   └── context
│
├── commands/
│   ├── help
│   ├── version
│   ├── rules
│   ├── language
│   ├── commands
│   └── ...
│
├── addons/
│   ├── discovery
│   ├── registry
│   ├── loader
│   ├── executor
│   └── api
│
├── programs/
│   ├── discovery
│   ├── registry
│   └── executor
│
├── languages/
│   ├── discovery
│   ├── loader
│   └── manager
│
├── config/
│
├── diagnostics/
│
├── version/
│
└── tests/
```

Esta estructura es conceptual.

El implementador puede modificarla si encuentra una arquitectura técnicamente mejor, siempre que mantenga las responsabilidades separadas.

---

# 22. Errores y códigos de salida

Los errores deben ser estructurados.

Como mínimo deben distinguirse:

```text
CLI usage error
Unknown command
Unknown option
Invalid argument
Addon not found
Program not found
Execution failure
Configuration error
Language error
File error
RtG validation error
Internal error
```

Los códigos de salida deben estar documentados.

No se debe depender de excepciones no controladas como interfaz pública.

---

# 23. Configuración

La configuración debe tener una ubicación y prioridad claramente definidas.

Debe determinarse la prioridad entre:

```text
Default
    ↓
Configuration file
    ↓
Environment
    ↓
Command-line arguments
```

La implementación final debe documentar qué nivel tiene prioridad.

---

# 24. Tests

La reconstrucción debe incluir pruebas automatizadas.

Como mínimo:

```text
tests/
├── cli/
├── parser/
├── commands/
├── addons/
├── programs/
├── languages/
├── configuration/
├── diagnostics/
└── version/
```

Deben probarse tanto casos válidos como inválidos.

Especialmente:

- comandos inexistentes;
- opciones inválidas;
- argumentos faltantes;
- addons inexistentes;
- ejecución correcta de addons;
- errores de addons;
- códigos de salida;
- idiomas inexistentes;
- configuración;
- `--help`;
- `--version`;
- compatibilidad de metadata.

---

# 25. Documentación

La reconstrucción debe dejar documentación suficiente para que otro desarrollador pueda entender el sistema sin leer todo el código.

Debe documentarse:

- arquitectura;
- CLI;
- parser;
- comandos;
- addons;
- program commands;
- idiomas;
- configuración;
- errores;
- versionado;
- tests;
- integración futura con RtG-Language.

---

# 26. Compatibilidad futura

RtG-CLI debe quedar preparado para:

```text
RtG-Language
    ↓
RtG Compiler
    ↓
RtG-CLI
    ↓
RtG-Format
```

pero **RtG-Language no debe implementarse dentro de esta reconstrucción salvo que sea necesario para establecer la interfaz de integración**.

Primero debe existir un contrato estable.

---

# 27. Qué NO hacer

Durante el trabajo:

- No inventar partes de RtG-Format.
- No asumir que el comportamiento actual es correcto.
- No conservar código únicamente porque ya existe.
- No eliminar funcionalidad sin revisar su propósito.
- No mezclar addons con el núcleo.
- No mezclar parsing con ejecución.
- No crear APIs implícitas.
- No duplicar información de versión sin necesidad.
- No crear sintaxis ambiguas.
- No implementar RtG-Language alrededor de una interfaz provisional.
- No integrar el RtG-Preview beta/obsoleto como si fuera el sistema moderno.
- No cambiar el formato RtG-Format para facilitar la CLI.

---

# 28. Objetivo final

Al terminar la reconstrucción, RtG-CLI debe ser:

```text
Formal
   +
Modular
   +
Extensible
   +
Documentado
   +
Testeado
   +
Predecible
   +
Compatible con RtG-Format
   +
Preparado para RtG-Language
```

El resultado debe ser una base sólida sobre la cual se pueda construir posteriormente:

```text
RtG-Language
RtG Compiler
RtG tools
RtG addons
RtG ecosystem
```

---

# 29. Orden de trabajo recomendado

Antes de implementar cambios importantes:

### Fase 1 — Auditoría

Revisar completamente el RtG-CLI existente:

```text
Código
Metadata
assets.json
Comandos
Addons
Program commands
Idiomas
Versiones
Tests
Documentación
```

### Fase 2 — Especificación

Definir formalmente:

```text
CLI contract
Command contract
Argument contract
Addon contract
Program command contract
Language contract
Configuration contract
Error contract
Version contract
```

### Fase 3 — Arquitectura

Separar los componentes y establecer las interfaces internas.

### Fase 4 — Implementación

Reconstruir el sistema utilizando la especificación anterior.

### Fase 5 — Tests

Crear pruebas para todos los componentes principales.

### Fase 6 — Documentación

Actualizar README, documentación técnica y ejemplos.

### Fase 7 — Integración futura

Comprobar que la arquitectura permite integrar RtG-Language sin rehacer RtG-CLI.

---

# 30. Criterio de finalización

RtG-CLI no debe considerarse terminado simplemente porque los comandos existentes vuelvan a funcionar.

Debe considerarse terminado cuando:

- la arquitectura esté definida;
- los comandos tengan contratos claros;
- los addons tengan API formal;
- los program commands tengan API formal;
- la ejecución real funcione;
- los argumentos no sean ambiguos;
- los idiomas tengan un sistema definido;
- la configuración esté definida;
- el versionado esté definido;
- los errores estén estructurados;
- exista cobertura de tests razonable;
- la documentación corresponda al código;
- no existan contradicciones conocidas con RtG-Format;
- exista una interfaz clara para la futura integración con RtG-Language.

---

## Estado actual

**RtG-CLI está pendiente de reconstrucción.**

Este README funciona como **documento de contexto inicial y contrato de diseño** antes de comenzar el trabajo.

Las decisiones que se descubran durante la auditoría deben documentarse y, cuando contradigan este documento, justificarse explícitamente antes de adoptarse.