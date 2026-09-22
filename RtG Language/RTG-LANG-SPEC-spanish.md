# RtG-Format — Especificación completa

## 1. Estructura general

```
Order
   "TypeA";
   "TypeB"
end

Object("TypeA")
   <secciones>
end

Object("TypeB")
   <secciones>
end
```

- `Order` declara en qué orden se deben cargar/procesar los tipos de
  objeto declarados más abajo. Es una lista de strings separadas por `;`
  (la última, sin `;`), cerrada con `end`.
- Cada `Object("Nombre")` agrupa un conjunto fijo de **secciones**, en
  cualquier orden: `global_properties`, `track`, `note-names`, `create`,
  `output`, `visualize` (esta última solo para preview de editor, no se
  interpreta).

## 2. Regla de cierre `end` / `end;;`

No es necesario memorizar cuándo usar `end;;` vs `end`. La regla real es
más simple: **`;` es terminador de sentencia/bloque, y puede repetirse
sin efecto** — el parser ignora cualquier cantidad de `;` (0, 1 o 2) tras
un `end`. Así que `end;;` es simplemente "`end` de este bloque + `;` que
cierra la sentencia del bloque padre" y funciona igual si escribes solo
`end` en todos lados. La convención `end;;` es solo higiene visual para
distinguir "aquí termina un sub-bloque, sigue otro" vs "aquí termina el
último".

## 3. Referencias a instancias

```
["NombreDeParte":N]
```
Es una **referencia a la instancia N (1-indexada) de la parte
"NombreDeParte"**. Se usa en `track/UUID`, `note-names` y `create`.

## 4. `global_properties`

```
global_properties
   { <objeto JSON literal> }
end
```
- El cuerpo es **siempre** un objeto JSON real y válido (no acepta la
  forma compacta `{ }` de una línea para reemplazar `end`, porque sus
  llaves ya son el JSON). **[supuesto: `global_properties` nunca usa la
  compactación de "un-liner"]**.
- Sirve para metadatos arbitrarios aplicados a **todas** las instancias
  del `Object` (no a una parte específica).

## 5. `track`

Declara cuántas instancias existen de cada parte, y cómo se agrupan bajo
un UUID compartido.

### 5.1 `track/object`
```
object
   "Seat":2;
   "Chassis":1
end
```
`"NombreParte":N` declara que existen `N` instancias de esa parte
(instancias `1..N`, 1-indexadas).

### 5.2 `track/UUID`
```
UUID
   ["Chassis":1] by {["Seat"x1]}
end
```
- `[ref] by {patrón}` declara que la instancia `ref` es la **raíz de un
  grupo UUID:** a esa instancia (y a las partes listadas en el patrón)
  se les asigna un identificador único compartido.
- `"NombreParte"xN` dentro del patrón = "reclama N instancias de esa
  parte por cada raíz". `xN` es opcional; si se omite, `x1` es el valor
  por defecto. **[supuesto — el propósito exacto de "compartir UUID" y
  cómo se reparten instancias cuando hay más de una raíz del mismo tipo
  de parte no quedó claro del ejemplo; confírmamelo]**

### 5.3 `track/properties`

```
properties
   ["Chassis":1]
      {
          "RGB":[0,255,0]
      }
   end
end
```
Cada entrada es `[ref] { JSON }` (uno o más, separados por `;` y `end`). Define
propiedades que sobrescriben, para esa instancia puntual, las de
`global_properties`. Las propiedades finales de cada instancia se
calculan como:
```
merge(global_properties, track/properties[esa instancia])
```
donde `track/properties` **gana** en caso de choque de claves. Si el
resultado combinado queda vacío, se serializa como `[]` (no `{}`) — así
sale en builds reales.

## 6. `note-names`

```
note-names
   ["Seat":1] --> "Piloto";
   ["Seat":2] --> "Señor volador OMG"
end
```
`[ref] --> "Etiqueta"` asocia un nombre legible (puramente descriptivo,
no afecta la generación) a una instancia.

## 7. `create`

Sección obligatoria antes de poder usar `output`. Tres formas de
sentencia, separadas por `;`:

1. **Instanciar sin conectar:**
   ```
   ["Chassis":1];
   ```
2. **Conectar — sintaxis real, `-a(b)->`**
   ```
   ["Seat":1] -1(18)-> ["Chassis":1];
   ```
   El `-` inicial es un delimitador literal, **no** un signo. La forma
   general es `-a(b)->`:
   - `a` = **tipo local de la conexión**. Si el objeto de origen tiene varios tipos posibles (p. ej. 1 y 3), aquí eliges cuál. 
     Es **opcional:** `-(b)->` (sin número) usa el tipo local por defecto.
   - `b` = **ID del punto de conexión** del objeto destino.

   En el build final ambos se serializan como el arreglo
   `[a, b, parent_id]`, con `a` y `b` como strings y `parent_id` como
   número (ver sección 12).
3. **Conectar con parámetros estructurados (offset + orientación):**
   ```
   ["Seat":2] -1{[0,0,0],[0,0,0,0,0,0]}-> ["Chassis":1]
   ```
   Misma sintaxis `-a{...}->`, pero en vez de `(b)` se usa `{ }` con dos
   arreglos: el primero `[x,y,z]` (offset de posición) y el segundo, de
   6 números (orientación/CFrame). **[pendiente: aún no tengo un
   ejemplo de esta forma en un build real, así que en el compilador
   actual `b` queda como objeto crudo `{"offset":[...], "orientation":[...]}`
   en vez de convertirse a string — dime cómo debe verse serializado]**

En los tres casos, `[ref]` a la izquierda es la parte que se crea/conecta
y `[ref]` a la derecha (tras `->`) es el destino de la conexión.

## 8. `output`

```
output
   cache("./CacheDelCarrito/");
   "./carro.json";
   "./carrito.txt"
end
```
- `output` es opcional, pero si aparece, **debe** venir después de
  `create` en el `Object` (no se puede exportar sin haber creado nada).
- `cache("ruta")`: define dónde se guarda el archivo `.rtg-cache` (debe
  ir primero si se usa).
- Cada string suelto declara un archivo a generar:
  - `.json` → JSON legible (pretty-printed).
  - `.txt` → el mismo JSON, codificado en Base64.
  - sin extensión → se trata como `.json`.
  - cualquier otra extensión → **error**.

## 12. El build final (formato real, confirmado por ti)

El resultado de compilar un `Object` **no** es un diccionario por tipo;
es un **arreglo plano** con una entrada por cada instancia creada, en el
orden en que aparecen como lado izquierdo en `create`:

```json
[
  ["Chassis", [], {"RGB":[0,255,0]}],
  ["Seat",    [["1","18",1]], {"RGB":[255,0,0]}],
  ["Seat",    [["1", {"offset":[0,0,0],"orientation":[0,0,0,0,0,0]}, 1]], {"RGB":[255,0,0]}]
]
```

Cada entrada es `[name, connections, properties]`:
- `name`: el nombre de la parte (`"Part"`, `"Anchor"`, `"Servo"`, etc.).
- `connections`: lista de `[a, b, parent_id]` — una por cada conexión
  saliente de esa instancia (puede haber varias). `parent_id` es el
  **índice 1-based de la instancia destino dentro de este mismo
  arreglo** (confirmado con tu build real: un id `22` apuntaba
  exactamente a la posición 22 del arreglo de 22 elementos).
- `properties`: `merge(global_properties, track/properties)` para esa
  instancia. Si queda vacío, se serializa como `[]` en vez de `{}`.

### Múltiples `Object` en un mismo archivo de salida
Si dos o más `Object` declaran el mismo archivo en su `output`, sus
arreglos se **concatenan** (en el orden de `Order`), y a los `parent_id`
internos de cada `Object` siguiente se les suma un **offset** = cantidad
de instancias ya escritas para ese archivo por los `Object` anteriores.
Ej.: si el primer `Object` aporta 5 instancias, los `parent_id` del
segundo `Object` se desplazan +5.
**[pendiente: esta regla la implementé según tu descripción pero aún no
la contrasté con un build real de dos `Object`; y no está definido qué
pasa si un `create` intenta apuntar a una instancia de OTRO `Object`
— por ahora el intérprete no lo permite]**

## 9. Comentarios

`// comentario` — desde `//` hasta el fin de línea. Válido al inicio de
una línea, después de `;`/`;;`, o en una línea vacía. No se interpretan
dentro de strings (`"// esto no es un comentario"`).

## 10. Forma de una sola línea (compactación)

Cualquier bloque `palabra ... end` puede escribirse como
`palabra{ ... }` (con o sin saltos de línea/espacios adentro):

```
create{ ["Chassis":1]; ["Seat":1] -1(18)-> ["Chassis":1] };;
```
es equivalente a:
```
create
   ["Chassis":1];
   ["Seat":1] -1(18)-> ["Chassis":1]
end;;
```
**Excepción:** `global_properties` no participa de esta compactación
porque su cuerpo ya usa `{ }` para el JSON (ver sección 4).

## 11. `visualize`

Reservado para mostrar una vista previa en editores de texto (extensión/
plugin). No afecta la generación — el intérprete lo ignora.

---

## Cosas que quedan por confirmar

1. Semántica exacta de los números en `-1(18)->` y en el arreglo de 6
   posiciones `{[x,y,z],[a,b,c,d,e,f]}->`.
2. Qué pasa si `track/UUID` referencia una parte que no tiene suficientes
   instancias declaradas en `track/object` para cubrir el patrón `xN`.
3. Si puede haber más de un `create`/`output` por `Object`, o solo uno.
4. Si los índices de `["Parte":N]` deben existir previamente en
   `track/object`, o si `create` puede "declarar sobre la marcha" una
   instancia no listada ahí.