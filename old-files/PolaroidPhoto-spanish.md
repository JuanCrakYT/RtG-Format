# RtG PolaroidPhoto Specification

> **Hecho por:** @JuanCrakYT
> **Documento:** Especificación Técnica de PolaroidPhoto (Ingeniería Inversa)
> **Juego Objetivo:** Road To Gramby's (Roblox)
> **Versión de la Especificación:** v1.000
> **Estado:** Documento Experimental / No Oficial
> **Fecha de actualización:** ...

---

## 1. Introducción

Qué es esta investigación y qué buscamos documentar.

### 1.1 Modelo conceptual del sistema

POLAROID PHOTO
├── TipoLocal
├── Conexiones
└── Propiedades
    ├── Phrase
    └── PhotoData
        ├── sceneCullObjects
        ├── cameraCF
        ├── sceneNewObjects
        └── sceneUpdateObjects

---

## 2. Estructura general

### 2.1 Estructura de PolaroidPhoto

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

### 2.2 Tupla de objeto

[TipoLocal, Conexiones, Propiedades]

---

## 3. Propiedades de PolaroidPhoto

### 3.1 Phrase

Confirmado.

Tipo: String

### 3.2 PhotoData

Confirmado.

Tipo: Object

---

## 4. Estructura de PhotoData

### 4.1 sceneCullObjects

Confirmado como campo existente.

### 4.2 cameraCF

Confirmado.

Tipo: CFrame serializado.

### 4.3 sceneNewObjects

Confirmado.

Tipo: Object.

### 4.4 sceneUpdateObjects

Confirmado.

Tipo: Array.

---

## 5. Estructura de Scene Objects

### 5.1 Objeto serializado

```json
{
    "className": "...",
    "children": [],
    "objectId": "...",
    "props": {}
}
```

### 5.2 className

### 5.3 objectId

### 5.4 children

### 5.5 props

---

## 6. Propiedades de objetos capturados

### 6.1 CFrame

### 6.2 Color

### 6.3 Material

### 6.4 Shape

### 6.5 Size

### 6.6 Transparency

### 6.7 Name

### 6.8 MeshId

### 6.9 TextureID

---

## 7. Objetos hijos

### 7.1 SpecialMesh

Propiedades observadas:

* Offset
* MeshType
* Scale
* MeshId
* TextureId

---

## 8. Tipos serializados

### 8.1 CFrame

### 8.2 Color3

### 8.3 Vector3

### 8.4 Enum

---

## 9. Assets y texturas

### 9.1 MeshId

### 9.2 TextureId

### 9.3 Referencias rbxassetid://

---

## 10. Cámara

### 10.1 cameraCF

### 10.2 Estructura del CFrame

### 10.3 Relación con la captura

---

## 11. Escena capturada

### 11.1 sceneNewObjects

### 11.2 sceneUpdateObjects

### 11.3 sceneCullObjects

---

## 12. Comportamiento observado

### 12.1 Renderizado de la escena

### 12.2 Tamaño de almacenamiento

### 12.3 "Too large"

### 12.4 Tiempo de desarrollo

### 12.5 Objetos fuera del encuadre

---

## 13. Sharecodes

### 13.1 Base64

### 13.2 Decodificación

### 13.3 Estructura resultante

---

## 14. Casos experimentales

### Experimento A: escena mínima

### Experimento B: un Part

### Experimento C: MeshPart

### Experimento D: textura

### Experimento E: distancia

### Experimento F: cámara

---

## 15. Descubrimientos confirmados

Lista acumulativa de todo lo que vayamos demostrando.

---

## 16. Investigación pendiente

Preguntas que todavía necesitamos resolver.

---

## 17. Ejemplos

### 17.1 PolaroidPhoto mínima

### 17.2 PolaroidPhoto con escena

### 17.3 Escena con MeshPart

---

## 18. Referencias

* Especímenes reales
* Wiki
* Experimentos
* Sharecodes
