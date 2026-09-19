# RtG PolaroidPhoto Specification

> **Hecho por:** @JuanCrakYT
> **Documento:** Especificación Técnica de PolaroidPhoto (Ingeniería Inversa)
> **Juego Objetivo:** Road To Gramby's (Roblox)
> **Versión de la Especificación:** v1.000
> **Estado:** Documento Experimental / No Oficial
> **Fecha de actualización:** 19/09/2026

---

## 1. Introducción

Esta investigación documenta la estructura interna de los objetos `PolaroidPhoto` utilizados por **Road To Gramby's**.
El objetivo es determinar mediante especímenes reales cómo se almacena una fotografía tomada con una Polaroid, incluyendo:

* El texto asociado a la fotografía.
* La posición y orientación de la cámara.
* Los objetos presentes en la escena capturada.
* Las propiedades visuales de dichos objetos.
* Las mallas y texturas utilizadas.
* Los objetos hijos.
* Los tipos de datos serializados.
* El comportamiento de la captura respecto al tamaño de la escena.
* La relación entre las fotografías y el sistema general de datos de RtG.

La investigación se basa principalmente en fotografías reales extraídas del juego y en la comparación entre diferentes especímenes.

No se utiliza **RtG-Preview** como fuente de información de esta especificación. La estructura documentada aquí procede de los datos reales de `PolaroidPhoto`.

---

### 1.1 Modelo conceptual del sistema

```tree
PolaroidPhoto
│
├── TipoLocal
├── Conexiones
└── Propiedades
    │
    ├── Phrase
    │
    └── PhotoData
        │
        ├── sceneCullObjects
        ├── cameraCF
        ├── sceneNewObjects
        └── sceneUpdateObjects
```

Una `PolaroidPhoto` es, por tanto, un objeto RtG normal cuya información fotográfica se encuentra principalmente dentro de `PhotoData`.

---

## 2. Estructura general

### 2.1 Estructura de PolaroidPhoto

La estructura mínima observada es:

```json
[
    [
        "PolaroidPhoto",
        [],
        {
            "Phrase": "...",
            "PhotoData": {}
        }
    ]
]
```

La estructura exterior sigue el formato general de RtG:

```json
[TipoLocal, Conexiones, Propiedades]
```

---

### 2.2 Tupla de objeto

La representación de la `PolaroidPhoto` utiliza la estructura:

```json
[TipoLocal, Conexiones, Propiedades]
```

Para una fotografía:

```js
TipoLocal = "PolaroidPhoto"
Conexiones = []
Propiedades = {
    Phrase,
    PhotoData
}
```

La información de la fotografía no se almacena como conexiones RtG normales, sino dentro de `PhotoData`.

---

## 3. Propiedades de PolaroidPhoto

### 3.1 Phrase

**Confirmado.**

`Phrase` es una cadena de texto asociada a la fotografía.

Tipo:

```md
String
```

Ejemplo:

```json
{
    "Phrase": "Your chill idea in the books"
}
```

La propiedad se encuentra directamente dentro de las propiedades de `PolaroidPhoto`, no dentro de `PhotoData`.

Durante la investigación se observaron diferentes frases entre fotografías, demostrando que el valor puede variar independientemente de la escena capturada.

---

### 3.2 PhotoData

**Confirmado.**

Tipo:

```md
Object
```

`PhotoData` contiene la información necesaria para reconstruir la escena representada por la fotografía.

Estructura observada:

```json
{
    "sceneCullObjects": [],
    "cameraCF": {
        "serializedType": "CFrame",
        "data": []
    },
    "sceneNewObjects": {},
    "sceneUpdateObjects": []
}
```

---

## 4. Estructura de PhotoData

### 4.1 sceneCullObjects

**Confirmado como campo existente.**

Tipo observado:

```md
Array
```

En los especímenes analizados:

```json
"sceneCullObjects": []
```

El campo existe incluso cuando no contiene elementos.

Su propósito exacto dentro del sistema de captura todavía no ha sido determinado completamente.

No debe interpretarse automáticamente como una lista de objetos que simplemente quedaron fuera del encuadre.

---

### 4.2 cameraCF

**Confirmado.**

Tipo:

```md
CFrame serializado
```

Ejemplo estructural:

```json
"cameraCF": {
    "serializedType": "CFrame",
    "data": [
        565.786376953125,
        55809.19921875,
        815.7516479492188,
        ...
    ]
}
```

`cameraCF` almacena la transformación espacial de la cámara utilizada para realizar la fotografía.

---

### 4.3 sceneNewObjects

**Confirmado.**

Tipo:

```md
Object
```

Contiene los objetos que fueron incluidos en la escena serializada de la fotografía.

Los identificadores aparecen como claves de objeto y los valores contienen la descripción serializada correspondiente.

Ejemplo estructural:

```json
"sceneNewObjects": {
    "4037": {
        "className": "Part",
        "children": {},
        "objectId": "4037",
        "props": {}
    }
}
```

Los IDs observados conservan valores numéricos asociados a los objetos originales de la escena.

---

### 4.4 sceneUpdateObjects

**Confirmado.**

Tipo:

```md
Array
```

En los especímenes analizados:

```json
"sceneUpdateObjects": []
```

Al igual que `sceneCullObjects`, el campo está presente aunque esté vacío.
No se ha demostrado que una fotografía normal necesite elementos dentro de este array.

---

## 5. Estructura de Scene Objects

### 5.1 Objeto serializado

Cada objeto dentro de `sceneNewObjects` utiliza una estructura equivalente a:

```json
{
    "className": "...",
    "children": {},
    "objectId": "...",
    "props": {}
}
```

Los campos observados son:

* `objectId`
* `className`
* `props`
* `children`

---

### 5.2 className

Identifica la clase del objeto serializado.
Entre las clases observadas en las fotografías se encuentran:

```md
Part
MeshPart
```

También se observaron objetos hijos de tipo:

```md
SpecialMesh
```

`className` no debe confundirse con el nombre concreto de una instancia.

---

### 5.3 objectId

Identificador del objeto dentro de la escena serializada.
Los especímenes demuestran que estos IDs pueden conservar valores elevados correspondientes a los objetos existentes en la escena original.
Por ejemplo, en la fotografía del trineo se observaron IDs en el rango aproximado:

```md
4037–4179
```

No todos los valores intermedios necesariamente aparecen.
Esto demuestra que `sceneNewObjects` no utiliza obligatoriamente una numeración nueva comenzando desde `1`.

---

### 5.4 children

Contiene los objetos hijos serializados.

Tipo observado:

```md
Object
```

Un caso especialmente importante es:

```md
Part
└── SpecialMesh
```

Los hijos permiten almacenar información que no pertenece directamente a las propiedades del objeto padre.

---

### 5.5 props

Contiene las propiedades serializadas del objeto.

Ejemplo conceptual:

```json
{
    "CFrame": {
        "serializedType": "CFrame",
        "data": []
    },
    "Color": {
        "serializedType": "Color3",
        "data": []
    },
    "Size": {
        "serializedType": "Vector3",
        "data": []
    }
}
```

Las propiedades dependen de la clase del objeto.

---

## 6. Propiedades de objetos capturados

Las siguientes propiedades fueron observadas directamente en los especímenes.

### 6.1 CFrame

**Confirmado.**

Representa la posición y orientación del objeto.

Se almacena mediante:

```json
{
    "serializedType": "CFrame",
    "data": [
        12 valores
    ]
}
```

La representación contiene:

```md
3 valores de posición
+
9 valores de matriz de rotación
```

---

### 6.2 Color

**Confirmado.**

Los colores se serializan mediante `Color3`.

Ejemplo:

```json
{
    "serializedType": "Color3",
    "data": [
        1,
        0,
        0
    ]
}
```

La representación observada utiliza el sistema de tipos serializados del formato.

---

### 6.3 Material

**Confirmado.**

Los objetos capturados pueden almacenar su material.

El valor se representa mediante un tipo serializado de enumeración.

---

### 6.4 Shape

**Confirmado en objetos que utilizan esta propiedad.**

La forma geométrica del `Part` puede aparecer dentro de `props`.
El valor se almacena como un tipo `Enum` serializado.

---

### 6.5 Size

**Confirmado.**

Los objetos pueden almacenar su tamaño mediante un `Vector3` serializado.

Estructura:

```json
{
    "serializedType": "Vector3",
    "data": [
        X,
        Y,
        Z
    ]
}
```

Ejemplo observado en el análisis del espécimen del trineo:

```json
[0.4, 0.4, 0.4]
```

para múltiples `MeshPart`.

---

### 6.6 Transparency

**Confirmado.**

Los objetos pueden almacenar su nivel de transparencia.
Se observaron múltiples objetos con valores diferentes de `0`.

En el espécimen de un trineo:

```md
14 objetos
```

presentaban `Transparency != 0`.

La transparencia puede aparecer tanto en objetos geométricos normales como en objetos utilizados para componentes especiales o colisiones.

---

### 6.7 Name

**Confirmado.**

Los objetos capturados conservan nombres de instancia.

Se observaron nombres como:

```md
TuneThing
Wheel
Body
Handle
Backwards
LegR
HeadCollider
ArmR
HandL
ArmL
HumanoidRootPart
LegL
Head
Display
HandR
Forwards
Volume
Tune
```

También existen numerosos objetos cuyo nombre es simplemente:

```md
Part
```

Esto demuestra que `Name` es independiente de `className`.

Por ejemplo:

```js
className = "MeshPart"
Name      = "Body"
```

---

### 6.8 MeshId

**Confirmado.**

Los `MeshPart` pueden almacenar directamente un `MeshId`.

En el espécimen del trineo se observaron múltiples MeshIds distintos, incluyendo:

```text
5866118755
6197105603
5798774379
5805830512
5895052281
5894541296
5808635639
5866220992
5825508409
5921427828
5808247738
5825174506
5826907083
5829281780
```

La cantidad de instancias de cada MeshId puede variar.

Ejemplo:

```md
5866118755 → 32 instancias
5805830512 → 10 instancias
```

---

### 6.9 TextureID

**Confirmado.**

Los objetos que utilizan texturas pueden almacenar referencias a assets mediante `TextureID`.

La representación observada utiliza referencias del tipo:

```md
rbxassetid://<ID>
```

Ejemplo conceptual:

```json
{
    "TextureID": "rbxassetid://123456789"
}
```

Los TextureID son referencias a assets externos y no representan directamente los datos binarios de la textura dentro del JSON.

---

## 7. Objetos hijos

### 7.1 SpecialMesh

`SpecialMesh` fue observado como objeto hijo de `Part`.

Estructura conceptual:

```tree
Part
└── SpecialMesh
```

Entre las propiedades observadas se encuentran:

* `Offset`
* `MeshType`
* `Scale`
* `MeshId`
* `TextureId`

Estas propiedades pertenecen al `SpecialMesh`, no al `Part` padre.

---

### 7.2 Scale de SpecialMesh

**Confirmado como propiedad del `SpecialMesh` observado.**

La existencia de:

```tree
SpecialMesh
└── Scale
```

no implica que un `Part` pueda ser escalado agregando:

```json
{
    "Scale": [3, 3, 3]
}
```

directamente a sus propiedades.

Son niveles diferentes de la estructura serializada.

Por lo tanto:

```md
Part.props.Scale
```

y:

```md
Part.children.SpecialMesh.props.Scale
```

no deben tratarse como equivalentes.

---

### 7.3 MeshId y TextureId de SpecialMesh

Un `SpecialMesh` puede contener sus propias referencias de malla y textura.

Esto permite diferenciar dos mecanismos:

```tree
MeshPart
├── MeshId
└── TextureID
```

frente a:

```tree
Part
└── SpecialMesh
    ├── MeshId
    └── TextureId
```

La diferencia debe conservarse al analizar fotografías.

---

## 8. Tipos serializados

El sistema utiliza objetos con un campo:

```json
{
    "serializedType": "...",
    "data": ...
}
```

### 8.1 CFrame

Estructura:

```json
{
    "serializedType": "CFrame",
    "data": [
        X,
        Y,
        Z,
        R1,
        R2,
        R3,
        R4,
        R5,
        R6,
        R7,
        R8,
        R9
    ]
}
```

Total:

```md
12 valores
```

---

### 8.2 Color3

Estructura:

```json
{
    "serializedType": "Color3",
    "data": [
        R,
        G,
        B
    ]
}
```

---

### 8.3 Vector3

Estructura:

```json
{
    "serializedType": "Vector3",
    "data": [
        X,
        Y,
        Z
    ]
}
```

---

### 8.4 Enum

Los valores enumerados utilizan una representación serializada mediante:

```json
{
    "serializedType": "Enum",
    "data": "..."
}
```

Esto se observó en propiedades como `Material` y `Shape`.

---

## 9. Assets y texturas

### 9.1 MeshId

Los MeshIds son referencias numéricas a assets de malla.
En una fotografía pueden aparecer múltiples instancias de una misma malla.

Por ejemplo:

```tree
MeshId
5866118755
├── instancia 1
├── instancia 2
├── ...
└── instancia 32
```

Por ello, contar MeshIds únicos no equivale a contar MeshParts.

---

### 9.2 TextureId

Las texturas se referencian mediante IDs de assets.
Pueden aparecer:

```md
MeshPart.props.TextureID
```

o:

```md
SpecialMesh.props.TextureId
```

El uso de `TextureID`/`TextureId` depende del objeto serializado.

Los IDs deben extraerse recorriendo recursivamente `sceneNewObjects` y sus `children`.

---

### 9.3 Referencias `rbxassetid://`

Las referencias de assets observadas utilizan la forma:

```md
rbxassetid://123456789
```

Para obtener el ID numérico:

```md
rbxassetid://123456789
        ↓
123456789
```

Las herramientas de análisis desarrolladas para esta investigación pueden extraer estos IDs automáticamente.

---

### 9.4 Relación MeshId → TextureId

Una fotografía puede contener información de malla y textura de manera separada.

Por ello, el análisis de assets debe distinguir:

```md
MeshId
TextureId
```

y no asumir:

```md
MeshId = TextureId
```

Una misma malla puede aparecer en varias instancias y las referencias visuales deben analizarse individualmente.

---

## 10. Cámara

### 10.1 cameraCF

`cameraCF` contiene la transformación espacial de la cámara utilizada durante la fotografía.

Está almacenado como un `CFrame` serializado.

---

### 10.2 Estructura del CFrame

La estructura observada es:

```json
[X, Y, Z,
 R1, R2, R3,
 R4, R5, R6,
 R7, R8, R9]
```

Los primeros tres valores corresponden a la posición.

Los nueve restantes corresponden a la matriz de orientación.

---

### 10.3 Relación con la captura

La cámara define la posición y orientación desde la que se realiza la fotografía.

Sin embargo, la existencia de un objeto dentro de `sceneNewObjects` no demuestra por sí sola que estuviera dentro del encuadre visible.
Los datos indican que la fotografía puede almacenar una escena considerablemente mayor que los elementos estrictamente visibles en la imagen.

---

## 11. Escena capturada

### 11.1 sceneNewObjects

Es el componente principal de la escena almacenada.
Contiene los objetos serializados que forman parte de la fotografía.

En el espécimen más grande analizado:

```md
143 objetos
```

distribuidos como:

```md
71 Part
72 MeshPart
```

Además, se observaron:

```md
9 SpecialMesh
```

como objetos hijos.

---

### 11.2 sceneUpdateObjects

Los especímenes estudiados presentaron:

```json
"sceneUpdateObjects": []
```

No se identificó todavía un caso de fotografía que requiera contenido dentro de este array.
Por ello se confirma su existencia, pero no se documenta todavía una semántica completa para sus elementos.

---

### 11.3 sceneCullObjects

Los especímenes estudiados presentaron:

```json
"sceneCullObjects": []
```

Se confirma el campo y su tipo, pero no se establece todavía una interpretación completa de su contenido.

---

## 12. Comportamiento observado

### 12.1 Renderizado de la escena

Una `PolaroidPhoto` no parece almacenar únicamente una imagen plana.

Los datos contienen una representación de objetos 3D:

```tree
objetos
├── posición
├── orientación
├── tamaño
├── color
├── material
├── transparencia
├── malla
├── textura
└── objetos hijos
```

Esto permite explicar por qué una fotografía puede contener una cantidad considerable de información.

---

### 12.2 Tamaño de almacenamiento

Las fotografías pueden consumir una cantidad considerable del almacenamiento de una partida.
El tamaño depende de la complejidad de la escena capturada.

Una escena con muchos objetos, MeshParts, mallas y texturas genera una cantidad mucho mayor de datos que una escena simple.

Durante la investigación se observaron fotografías con porcentajes de almacenamiento muy elevados.
Esto concuerda con la estructura descubierta: la fotografía almacena datos de la escena, no simplemente los píxeles de una imagen.

---

### 12.3 "Too large"

Las fotografías pueden llegar a ser suficientemente grandes como para provocar problemas relacionados con el tamaño del guardado.

Se documentaron casos comunitarios en los que fotografías de escenas grandes consumían una proporción considerable del almacenamiento disponible.
Por tanto:

```md
más objetos capturados
        ↓
más datos serializados
        ↓
mayor tamaño de la PolaroidPhoto
```

---

### 12.4 Tiempo de desarrollo

La complejidad de una fotografía depende directamente de la escena capturada.

Una fotografía aparentemente sencilla puede contener numerosos objetos.

El espécimen del trineo desmontado demuestra que la captura puede incluir:

* piezas físicas;
* MeshParts;
* componentes del personaje;
* objetos transparentes;
* objetos con texturas;
* objetos con nombres específicos;
* objetos hijos.

---

### 12.5 Objetos fuera del encuadre

La evidencia disponible indica que la escena almacenada puede contener objetos que no son necesariamente los elementos principales visibles en el encuadre.
Esto es consistente con observaciones comunitarias de que las PolaroidPhotos pueden incluir elementos alrededor de la zona fotografiada.

No obstante, `sceneNewObjects` no debe interpretarse simplemente como "objetos visibles".

La relación exacta entre:

```md
campo de visión
sceneNewObjects
sceneCullObjects
```

requiere experimentos adicionales.

---

## 13. Sharecodes

### 13.1 Base64

Los Sharecodes de RtG pueden utilizar Base64 para representar datos serializados.
Ejemplo de estructura conceptual:

```md
JSON
 ↓
UTF-8
 ↓
Base64
 ↓
Sharecode
```

---

### 13.2 Decodificación

Al decodificar un Sharecode se puede obtener una representación JSON del objeto o conjunto de objetos correspondiente.

La investigación del formato general de RtG demuestra que Base64 puede utilizarse para transportar estructuras de creación.

---

### 13.3 Estructura resultante

No debe confundirse un Sharecode de:

```md
PolaroidCamera
```

con uno de:

```md
PolaroidPhoto
```

Durante la investigación se identificó un Sharecode correspondiente a:

```json
[["PolaroidCamera", [], []]]
```

Esto demuestra la representación Base64 del objeto `PolaroidCamera`, pero **no constituye un ejemplo de PhotoData de `PolaroidPhoto`**.

También existen referencias comunitarias históricas a modificaciones de fotografías mediante Base64, pero no se conserva un espécimen histórico suficientemente verificable como para documentar una sintaxis específica adicional.

---

## 14. Casos experimentales

### Experimento A: escena mínima

**Objetivo:** determinar la estructura mínima de una `PolaroidPhoto`.

**Resultado:**

Se confirmó que la estructura exterior requiere:

```tree
PolaroidPhoto
├── Conexiones
└── Propiedades
    ├── Phrase
    └── PhotoData
```

---

### Experimento B: un Part

**Objetivo:** determinar cómo se serializa un objeto geométrico básico.

**Resultado:**

Se observaron propiedades como:

```md
CFrame
Color
Material
Shape
Size
Transparency
Name
```

El objeto aparece dentro de:

```tree
PhotoData
└── sceneNewObjects
```

---

### Experimento C: MeshPart

**Objetivo:** determinar cómo se representan objetos con malla integrada.

**Resultado:**

Los `MeshPart` almacenan referencias de malla mediante:

```md
MeshId
```

y pueden almacenar referencias de textura mediante:

```md
TextureID
```

---

### Experimento D: textura

**Objetivo:** determinar cómo aparecen las texturas.

**Resultado:**

Se identificaron referencias:

```md
TextureID
```

y, en `SpecialMesh`:

```md
TextureId
```

con referencias `rbxassetid://`.

---

### Experimento E: distancia

**Objetivo:** observar cómo cambia el contenido de una fotografía al variar la distancia respecto a la escena.

**Resultado observado:**

Las fotografías pueden incorporar cantidades importantes de objetos incluso cuando la captura parece visualmente sencilla.
Se observaron diferencias de tamaño de almacenamiento asociadas al área/escena fotografiada.

La relación matemática exacta entre distancia, área y objetos incluidos todavía no está establecida.

---

### Experimento F: cámara

**Objetivo:** determinar cómo se almacena la posición de la cámara.

**Resultado:**

La fotografía contiene:

```md
PhotoData.cameraCF
```

como un `CFrame` serializado de 12 valores.

---

### Experimento G: escena compleja

**Objetivo:** estudiar una fotografía con una gran cantidad de objetos.
**Especimen principal:** fotografía del trineo completamente desmontado.
**Resultado:**

```tree
143 objetos
├── 71 Part
└── 72 MeshPart
```

Además:

```md
9 SpecialMesh
72 objetos con MeshId
14 MeshId únicos
14 objetos con Transparency != 0
```

La fotografía contiene también componentes reconocibles del personaje y numerosos objetos nombrados individualmente.
Este espécimen es actualmente la referencia principal para estudiar escenas complejas.

---

### Experimento H: comparación entre fotografías

Se compararon varios especímenes:

```md
Photos/1.json
Photos/2.json
Photos/3.json
Photos/new.json
PolaroidPhoto.json
```

Las fotografías presentan la misma estructura general:

```tree
PolaroidPhoto
└── PhotoData
    ├── sceneCullObjects
    ├── cameraCF
    ├── sceneNewObjects
    └── sceneUpdateObjects
```

La cantidad de objetos, frases, cámaras, meshes y transparencias cambia entre especímenes.

Esto demuestra que la estructura es reutilizable y no depende de una escena específica.

---

## 15. Descubrimientos confirmados

### Estructura

* `PolaroidPhoto` es un `TipoLocal` válido.
* Utiliza la estructura general `[TipoLocal, Conexiones, Propiedades]`.
* `Phrase` existe directamente dentro de las propiedades.
* `PhotoData` existe dentro de las propiedades.
* `PhotoData` contiene `sceneCullObjects`.
* `PhotoData` contiene `cameraCF`.
* `PhotoData` contiene `sceneNewObjects`.
* `PhotoData` contiene `sceneUpdateObjects`.

### Scene Objects

* `sceneNewObjects` es un objeto/diccionario.
* Los objetos poseen `objectId`.
* Los objetos poseen `className`.
* Los objetos poseen `props`.
* Los objetos poseen `children`.
* Se observaron `Part`.
* Se observaron `MeshPart`.
* Se observaron `SpecialMesh` como objetos hijos.
* Los IDs de los objetos pueden conservar valores correspondientes a la escena original.

### Propiedades

Se observaron:

```md
CFrame
Color
Material
Shape
Size
Transparency
Name
MeshId
TextureID
```

### Serialización

Se confirmaron los tipos:

```md
CFrame
Color3
Vector3
Enum
```

mediante el sistema:

```json
{
    "serializedType": "...",
    "data": ...
}
```

### Mallas y texturas

* `MeshPart` puede almacenar `MeshId`.
* `MeshPart` puede almacenar `TextureID`.
* `SpecialMesh` puede almacenar `MeshId`.
* `SpecialMesh` puede almacenar `TextureId`.
* `SpecialMesh` puede almacenar `Scale`.
* Las referencias de textura utilizan `rbxassetid://`.
* Una fotografía puede contener múltiples MeshIds.
* Una fotografía puede contener múltiples instancias de una misma malla.

### Escena

* Una `PolaroidPhoto` almacena información de una escena 3D.
* No es simplemente una imagen plana.
* Una fotografía puede contener muchos objetos.
* Las escenas grandes pueden producir fotografías de gran tamaño.
* Los objetos transparentes también pueden ser serializados.
* Los objetos fuera del elemento principal de interés pueden formar parte de la escena serializada.

---

## 16. Investigación pendiente

Los siguientes puntos no se consideran resueltos en v1.000.

### 16.1 sceneCullObjects

Determinar exactamente:

```md
qué representa cada entrada
```

y cuándo se genera.

---

### 16.2 sceneUpdateObjects

Determinar:

```md
qué objetos aparecen aquí
```

y en qué circunstancias.

---

### 16.3 Criterio de selección de objetos

Determinar exactamente qué regla utiliza la Polaroid para decidir:

```md
qué objetos entran en sceneNewObjects
```

Especialmente en relación con:

```md
distancia
campo de visión
oclusiones
objetos transparentes
objetos detrás de la cámara
```

---

### 16.4 Texturas

Determinar si existen otras formas de referencia a texturas además de:

```md
TextureID
TextureId
```

y localizar todas las texturas utilizadas por una fotografía.

---

### 16.5 SpecialMesh

Investigar completamente:

```md
Offset
MeshType
Scale
MeshId
TextureId
```

y determinar cómo interactúan entre sí.

---

### 16.6 Cámara

Determinar experimentalmente si `cameraCF` corresponde exactamente al:

```md
CFrame de la cámara
```

en el momento de la captura y si existen transformaciones adicionales aplicadas durante el proceso.

---

### 16.7 IDs

Determinar exactamente de dónde proceden los `objectId` de `sceneNewObjects` y bajo qué circunstancias aparecen huecos en la numeración.

---

### 16.8 Almacenamiento

Establecer una relación cuantitativa entre:

```md
cantidad de objetos
MeshParts
MeshIds
TextureIds
tamaño del JSON
tamaño del guardado
```

---

### 16.9 Propiedades adicionales

Buscar propiedades que todavía no hayan aparecido en los especímenes disponibles.

---

## 17. Ejemplos

### 17.1 PolaroidPhoto mínima

Estructura conceptual:

```json
[
    [
        "PolaroidPhoto",
        [],
        {
            "Phrase": "",
            "PhotoData": {
                "sceneCullObjects": [],
                "cameraCF": {
                    "serializedType": "CFrame",
                    "data": [
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1
                    ]
                },
                "sceneNewObjects": {},
                "sceneUpdateObjects": []
            }
        }
    ]
]
```

> Este ejemplo representa la estructura documentada. No debe interpretarse como una garantía de que una fotografía artificial con esta estructura pueda ser aceptada por el juego.

---

### 17.2 PolaroidPhoto con escena

Estructura conceptual:

```json
[
    [
        "PolaroidPhoto",
        [],
        {
            "Phrase": "Example",
            "PhotoData": {
                "sceneCullObjects": [],
                "cameraCF": {
                    "serializedType": "CFrame",
                    "data": [
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1
                    ]
                },
                "sceneNewObjects": {
                    "100": {
                        "objectId": "100",
                        "className": "Part",
                        "props": {},
                        "children": {}
                    }
                },
                "sceneUpdateObjects": []
            }
        }
    ]
]
```

---

### 17.3 Escena con MeshPart

Ejemplo conceptual de la estructura observada:

```json
{
    "objectId": "100",
    "className": "MeshPart",
    "props": {
        "MeshId": "123456789",
        "TextureID": "rbxassetid://987654321"
    },
    "children": {}
}
```

Los valores anteriores son únicamente ilustrativos; no representan una combinación real específica de asset IDs.

---

### 17.4 Part con SpecialMesh

Estructura conceptual:

```json
{
    "objectId": "100",
    "className": "Part",
    "props": {},
    "children": {
        "101": {
            "objectId": "101",
            "className": "SpecialMesh",
            "props": {
                "MeshId": "...",
                "TextureId": "...",
                "Scale": {
                    "serializedType": "Vector3",
                    "data": [
                        1,
                        1,
                        1
                    ]
                }
            },
            "children": {}
        }
    }
}
```

La presencia de `Scale` aquí corresponde al `SpecialMesh` y no demuestra que exista una propiedad de escala equivalente directamente en `Part`.

---

## 18. Referencias

### Especímenes reales

* `dev/Photos/1.json`
* `dev/Photos/1org.json`
* `dev/Photos/2.json`
* `dev/Photos/2org.json`
* `dev/Photos/3.json`
* `dev/Photos/3org.json`
* `dev/Photos/new.json`
* `dev/PolaroidPhoto.json`
* `dev/PolaroidPhoto_Organized.json`

### Herramientas de investigación

* `dev/organize_polaroid.py`
* `dev/scripts/textures/TextureId.py`
* `dev/scripts/textures/openTexturesID.py`
* `dev/scripts/openAssetID.py`
* `dev/scripts/launcher.py`

Estas herramientas se utilizan para organizar especímenes y extraer referencias de assets y texturas.

### Fuentes de investigación

* Especímenes reales de `PolaroidPhoto`.
* Comparación entre fotografías tomadas en diferentes escenas.
* Ingeniería inversa del formato de guardado de RtG.
* Observaciones experimentales dentro del juego.
* Observaciones de la comunidad sobre almacenamiento y comportamiento de PolaroidPhotos.

---

## Estado de la especificación

**v1.000 — Estructura principal documentada.**

La estructura fundamental de `PolaroidPhoto` se considera suficientemente establecida para documentarse como especificación experimental:

```tree
PolaroidPhoto
│
├── Phrase
│
└── PhotoData
    │
    ├── sceneCullObjects
    ├── cameraCF
    ├── sceneNewObjects
    │   │
    │   └── Scene Object
    │       ├── objectId
    │       ├── className
    │       ├── props
    │       └── children
    │
    └── sceneUpdateObjects
```

La investigación futura debe concentrarse principalmente en **el criterio de captura de objetos, `sceneCullObjects`, `sceneUpdateObjects`, las referencias completas de texturas y el comportamiento exacto de la escena respecto a la cámara**.
