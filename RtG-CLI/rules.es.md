# Reglas de comandos de RtG-CLI

## 1. Estructura general

Un comando de RtG-CLI está formado por un comando principal y, opcionalmente, argumentos.

Formato general:

`rtg <comando> [<argumentos>]`

El primer argumento después de `rtg` determina qué comando o addon se ejecutará.

Ejemplos:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Comandos registrados

Los comandos principales deben estar registrados en la configuración de RtG-CLI.

Un comando se identifica mediante su clave interna.

Ejemplo:

`image`

La clave `image` identifica al addon correspondiente, independientemente del nombre mostrado al usuario.

Ejemplo:

`image` → `RtG Image`

`preview` → `RtG Preview`

El nombre mostrado no debe utilizarse como identificador del comando.

---

## 3. Comandos de RtG-CLI y comandos de los addons

RtG-CLI y sus addons pueden tener comandos o argumentos propios.

Los argumentos pertenecientes directamente a RtG-CLI utilizan una sola raya (`-`) al comienzo.

Los argumentos pertenecientes a un addon no pueden utilizar una sola raya (`-`) al comienzo.

Esto permite diferenciar los argumentos del sistema de los argumentos propios de un addon.

Ejemplo correcto:

`rtg help image -lang`

`-lang` pertenece a RtG-CLI.

Ejemplo incorrecto:

`rtg image -width`

Si `-width` pertenece a RtG Image, no debe comenzar con una sola raya.

---

## 4. Argumentos del sistema

Los argumentos del sistema utilizan una sola raya (`-`) o la sintaxis correspondiente definida por RtG-CLI.

Ejemplos:

`-v`

`--version`

`-h`

`--help`

`-lang`

`-en`

Los argumentos del sistema pueden aparecer después del comando al que afectan.

Ejemplo:

`rtg help image -en`

En este caso:

* `help` es un comando de RtG-CLI.
* `image` identifica el addon.
* `-en` es un argumento de RtG-CLI.
* `-en` no pertenece a RtG Image.

---

## 5. Posición de los argumentos del sistema

Los argumentos del sistema no deben aparecer antes del comando o addon al que afectan cuando dicho argumento depende de ese comando.

Ejemplo correcto:

`rtg help image -en`

Ejemplo incorrecto:

`rtg help -en image`

La posición debe permitir determinar claramente qué comando recibe el argumento.

---

## 6. Comandos y argumentos de los addons

Los addons pueden definir sus propios comandos y argumentos.

Los comandos de un addon deben ser una sola palabra y no deben contener espacios.

Ejemplo correcto:

`rtg image convert`

Ejemplo incorrecto:

`rtg image convert image`

Si un addon necesita representar una operación compuesta, debe utilizar argumentos separados en lugar de crear un comando que contenga espacios.

---

## 7. Uso de guiones en comandos de addons

Un comando o argumento propio de un addon no debe comenzar con una sola raya (`-`).

Si un addon necesita utilizar una opción con guiones, debe utilizar una sintaxis diferente a la reservada por RtG-CLI.

Por ejemplo:

`--width`

es válido como opción propia de un addon.

Mientras que:

`-width`

está reservado para opciones del sistema.

Los nombres que no necesiten guiones pueden utilizarse normalmente:

`convert`

`export`

`preview`

---

## 8. Los comandos de addons no pueden utilizar espacios

Los comandos de addons deben representar una única unidad.

Correcto:

`rtg image convert`

Incorrecto:

`rtg image convert image`

Incorrecto:

`rtg image create new image`

Los argumentos separados deben escribirse como argumentos independientes.

---

## 9. Idiomas

Los idiomas disponibles de un addon se definen mediante su configuración.

Ejemplo:

`lang: ["es", "en"]`

Los textos traducidos se identifican mediante el código correspondiente al idioma.

Ejemplo:

`content.es`

`content.en`

El selector de idioma utilizado por RtG-CLI debe considerarse un argumento del sistema.

Ejemplo:

`rtg help image -en`

---

## 10. El idioma no cambia el comando

Cambiar el idioma solamente modifica el texto mostrado por RtG-CLI.

No cambia el nombre interno del comando.

Ejemplo:

`rtg help image -es`

y

`rtg help image -en`

siguen haciendo referencia al mismo comando:

`image`

---

## 11. Ayuda

La ayuda general se obtiene mediante:

`rtg help`

La ayuda de un comando específico se obtiene mediante:

`rtg help <comando>`

La ayuda puede solicitarse en un idioma específico:

`rtg help <comando> -<idioma>`

Ejemplo:

`rtg help image -en`

---

## 12. Consulta de idiomas

Los idiomas disponibles para un addon pueden consultarse mediante:

`rtg help <comando> -lang`

Ejemplo:

`rtg help image -lang`

Esta opción pertenece a RtG-CLI y no al addon.

---

## 13. Los addons no deben modificar las reglas del sistema

Un addon puede definir sus propios comandos y argumentos, pero no puede redefinir el significado de los argumentos reservados por RtG-CLI.

Por ejemplo, un addon no debe utilizar `-h` para darle un significado diferente a la ayuda del sistema.

Los nombres reservados por RtG-CLI tienen prioridad sobre los comandos de los addons.

---

## 14. Separación entre identificación y nombre

La clave interna del addon es utilizada para identificarlo.

El nombre del addon solamente se utiliza como información descriptiva o para mostrarlo al usuario.

Ejemplo:

`image` → identificador interno

`RtG Image` → nombre mostrado

No debe asumirse que el nombre mostrado puede utilizarse como comando.

---

## 15. Los comandos deben ser deterministas

RtG-CLI debe poder determinar si un argumento pertenece al sistema o al addon sin depender del nombre descriptivo del programa.

La interpretación debe basarse en la estructura y las reglas del comando.

Ejemplo:

`rtg help image -en`

debe interpretarse siempre de la misma manera:

`rtg` → CLI

`help` → comando del CLI

`image` → addon

`-en` → opción del CLI

---

## 16. Argumentos desconocidos

Si RtG-CLI recibe un argumento reservado para el sistema que no reconoce, debe informar que la opción no existe.

Si un argumento pertenece al addon, RtG-CLI debe permitir que el addon lo procese según las reglas y comandos definidos por dicho addon.

RtG-CLI no debe inventar el significado de argumentos que no estén definidos.

---

## 17. No asumir comandos que no estén registrados

RtG-CLI no debe considerar válido un comando solamente porque exista una carpeta, archivo o programa relacionado.

El comando debe estar definido en la configuración correspondiente.

---

## 18. Compatibilidad

Los addons deben respetar las reglas de sintaxis de RtG-CLI para poder integrarse correctamente.

Un addon puede tener una implementación interna completamente diferente, pero su interfaz de comandos debe respetar las reglas establecidas por RtG-CLI.

---

## 19. Regla de prioridad

Cuando exista una colisión entre una opción del sistema y una opción de un addon, la opción reservada por RtG-CLI tiene prioridad.

Los addons no pueden apropiarse de comandos o argumentos reservados por el sistema.

---

## 20. Ejemplos completos

Comando de addon:

`rtg image`

Ayuda:

`rtg help image`

Ayuda en inglés:

`rtg help image -en`

Consultar idiomas:

`rtg help image -lang`

Versión del CLI:

`rtg --version`

Ayuda del CLI:

`rtg --help`

Una opción propia del addon:

`rtg image --width 128`

Una opción propia del addon con valor:

`rtg image --output archivo.json`

Una combinación:

`rtg image archivo.png --output archivo.json`

En este último ejemplo:

* `image` identifica el addon.
* `archivo.png` es un argumento del addon.
* `--output` es una opción del addon.
* `archivo.json` es el valor de esa opción.
* Ninguno de esos argumentos debe ser interpretado como una opción del sistema.
