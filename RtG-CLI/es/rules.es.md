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

RtG-CLI y los addons pueden tener sus propios comandos y argumentos.

Antes de identificar un addon, los comandos y argumentos pertenecen a RtG-CLI.
Después de identificar un addon, el prefijo determina a quién pertenece cada argumento:

- Sin raya (`-`) → pertenece al addon.
- Dos rayas (`--`) → pertenece al addon.
- Una raya (`-`) → pertenece a RtG-CLI.

Ejemplo:

`rtg image convert`

- `image` → addon.
- `convert` → comando del addon.

Ejemplo:

`rtg image --width 128`

- `image` → addon.
- `--width` → argumento del addon.
- `128` → valor del argumento del addon.

Ejemplo:

`rtg image -lang`

- `image` → addon.
- `-lang` → argumento de RtG-CLI.

---

## 4. Argumentos del sistema

Antes de identificar un addon, RtG-CLI utiliza sus propias reglas de sintaxis.
Las opciones largas del sistema utilizan dos rayas:

`rtg --version`
`rtg --help`

Las abreviaturas del sistema utilizan una raya:

`rtg -v`
`rtg -h`
`rtg -l`

Después de identificar un addon, una opción que comienza con una sola raya (`-`) pertenece a RtG-CLI.

Ejemplo:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumentos antes y después del addon

Los argumentos de RtG-CLI pueden tener un significado diferente dependiendo de si se encuentran antes o después de identificar el addon.

Antes de identificar un addon, los argumentos pertenecen a RtG-CLI.

Por ejemplo:

`rtg --lang`

Muestra los idiomas disponibles para RtG-CLI.

Después de identificar un addon, los argumentos se interpretan según las reglas de propiedad establecidas para los addons.

Por ejemplo:

`rtg image -lang`

Consulta los idiomas disponibles para el addon `image`.

De esta forma, la posición del argumento determina su contexto y evita confundir los argumentos globales de RtG-CLI con los argumentos utilizados después de identificar un addon.

---

## 6. Posición de los argumentos del sistema

Los argumentos del sistema no deben aparecer antes del comando o addon al que afectan cuando dicho argumento depende de ese comando.

Ejemplo correcto:

`rtg help image -en`

Ejemplo incorrecto:

`rtg help -en image`

La posición debe permitir determinar claramente qué comando recibe el argumento.

---

## 7. Comandos y argumentos de los addons

Los comandos se escriben como argumentos individuales de la terminal.

Un comando no debe contener espacios sin estar entre comillas.

Los argumentos posteriores pueden ser utilizados por el addon según su propia interfaz.

Por ejemplo:

`rtg image convert image`

puede interpretarse como:

- `image` → addon
- `convert` → comando del addon
- `image` → argumento del comando

---

## 8. Uso de guiones en comandos de addons

Después de identificar un addon:

- Los argumentos sin raya pertenecen al addon.
- Los argumentos con dos rayas o más (`--`) pertenecen al addon.
- Los argumentos con una sola raya (`-`) pertenecen a RtG-CLI.

Ejemplos:

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Los comandos de addons no pueden utilizar espacios

Los comandos de addons deben representar una única unidad.

Correcto:

`rtg image convert`

Incorrecto:

`rtg image convert image`

Incorrecto:

`rtg image create new image`

Los argumentos separados deben escribirse como argumentos independientes.

---

## 10. Idiomas

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

## 11. El idioma no cambia el comando

Cambiar el idioma solamente modifica el texto mostrado por RtG-CLI.

No cambia el nombre interno del comando.

Ejemplo:

`rtg help image -es`

y

`rtg help image -en`

siguen haciendo referencia al mismo comando:

`image`

---

## 12. Ayuda

La ayuda general se obtiene mediante:

`rtg help`

La ayuda de un comando específico se obtiene mediante:

`rtg help <comando>`

La ayuda puede solicitarse en un idioma específico:

`rtg help <comando> -<idioma>`

Ejemplo:

`rtg help image -en`

---

## 13. Consulta de idiomas

Los idiomas disponibles para un addon pueden consultarse mediante:

`rtg help <comando> -lang`

Ejemplo:

`rtg help image -lang`

Esta opción pertenece a RtG-CLI y no al addon.

---

## 14. Los addons no deben modificar las reglas del sistema

Un addon puede definir sus propios comandos y argumentos, pero no puede redefinir el significado de los argumentos reservados por RtG-CLI.

Por ejemplo, un addon no debe utilizar `-h` para darle un significado diferente a la ayuda del sistema.

Los nombres reservados por RtG-CLI tienen prioridad sobre los comandos de los addons.
Los comandos y opciones reservados por RtG-CLI deben estar definidos explícitamente por la interfaz del CLI.

Un addon no puede redefinir el comportamiento de una opción reservada.

---

## 15. Separación entre identificación y nombre

La clave interna del addon es utilizada para identificarlo.

El nombre del addon solamente se utiliza como información descriptiva o para mostrarlo al usuario.

Ejemplo:

`image` → identificador interno

`RtG Image` → nombre mostrado

No debe asumirse que el nombre mostrado puede utilizarse como comando.

---

## 16. Los comandos deben ser deterministas

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

## 17. Argumentos desconocidos

Después de identificar un addon, RtG-CLI debe determinar la propiedad de cada argumento según su prefijo.

- Un argumento sin raya pertenece al addon.
- Un argumento con dos rayas o más (`--`) pertenece al addon.
- Un argumento con una sola raya (`-`) pertenece a RtG-CLI.

Si RtG-CLI recibe un argumento propio del sistema que no reconoce, debe informar que la opción no existe.

Los argumentos del addon deben ser entregados al addon sin que RtG-CLI intente interpretar su significado.

---

## 18. No asumir comandos que no estén registrados

RtG-CLI no debe considerar válido un comando solamente porque exista una carpeta, archivo o programa relacionado.

El comando debe estar definido en la configuración correspondiente.

---

## 19. Compatibilidad

Los addons deben respetar las reglas de sintaxis de RtG-CLI para poder integrarse correctamente.

Un addon puede tener una implementación interna completamente diferente, pero su interfaz de comandos debe respetar las reglas establecidas por RtG-CLI.

---

## 20. Regla de prioridad

Después de identificar un addon, una sola raya (`-`) está reservada para RtG-CLI.
Un addon no puede utilizar argumentos que comiencen con una sola raya.

Los argumentos que comiencen con dos o más rayas (`--`) o que no comiencen con raya pertenecen al addon.

---

## 21. Argumentos del addon

Una vez identificado el addon, RtG-CLI no debe asumir el significado de los argumentos específicos del addon.

Los argumentos que pertenezcan al addon deben ser entregados al programa del addon para que este los procese.

Ejemplo:

`rtg image --width 128`

RtG-CLI identifica `image` como addon.

`--width 128` corresponde a la interfaz de RtG Image y debe ser procesado por dicho addon.

---

## 22. Argumentos con espacios

Los argumentos que contengan espacios deben escribirse entre comillas para que la terminal los trate como un único argumento.

Ejemplo:

`rtg image "C:\Users\User\Downloads\mi imagen.png" "C:\Users\User\Downloads\salida.json"`

La ruta completa debe recibirse como un único argumento.

---

## 23. Los argumentos del addon deben conservarse

RtG-CLI no debe modificar, eliminar ni reinterpretar argumentos destinados al addon, salvo cuando una regla explícita del sistema indique lo contrario.

Los argumentos deben entregarse al addon en el orden en que fueron proporcionados por el usuario.

---

## 24. Ejemplos completos

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

En este ejemplo:

* `image` identifica el addon.
* `archivo.png` es un argumento del addon.
* `--output` es una opción del addon.
* `archivo.json` es el valor de esa opción.
* Ninguno de esos argumentos debe ser interpretado como una opción del sistema.
