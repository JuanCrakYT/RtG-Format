# Ayuda de RtG-CLI

RtG-CLI es el intermediario entre el usuario y los addons de RtG.

## Uso

```text
rtg [opciones] <comando> [<argumentos>]
```

El primer argumento identifica el comando o addon que se utilizará.

Ejemplos:

```text
rtg image
rtg preview
rtg help image
```

## Comandos principales

```text
rtg help <comando>
```

Muestra la ayuda de un comando o addon.

```text
rtg help <comando> -<idioma>
```

Muestra la ayuda del comando en un idioma específico.

```text
rtg help <comando> -lang
```

Muestra los idiomas disponibles para ese addon.

## Opciones del sistema

```text
-v, --version    Muestra la versión de RtG-CLI.
-h, --help       Muestra la ayuda.
-l, --lang       Consulta los idiomas de RtG-CLI.
-r, --rules      Muestra las reglas de RtG-CLI.
```


Ejemplos:

```text
rtg --version
rtg -h
rtg --lang
rtg --rules
```

## Idiomas

Los idiomas se indican mediante una sola raya (`-`).

```text
rtg help image -es
rtg help image -en
```

El idioma utilizado no cambia el nombre del comando.

Para consultar los idiomas disponibles de un addon:

```text
rtg help image -lang
```

## Argumentos de los addons

Después de identificar un addon, los argumentos se separan según su prefijo:

```text
sin raya       → addon
--argumento    → addon
-argumento     → RtG-CLI
```

Ejemplos:

```text
rtg image convert
rtg image --width 128
rtg image -lang
```

En:

```text
rtg image --width 128
```

`image` identifica el addon y `--width 128` se entrega al addon para que lo procese.

En:

```text
rtg image -lang
```

`-lang` pertenece a RtG-CLI y consulta los idiomas del addon.

## Argumentos con espacios

Los argumentos que contienen espacios deben escribirse entre comillas.

Ejemplo:

```text
rtg image "mi imagen.png"
```

RtG-CLI conserva los argumentos del addon y los entrega en el mismo orden en que fueron escritos.

## Reglas

Para consultar las reglas completas:

```text
rtg -r
rtg --rules
```

También puede especificarse un idioma:

```text
rtg -r -es
rtg --rules -en
```

Si no se especifica un idioma, se utilizará el primer idioma definido en `assets.json`.

## Más información

Para obtener ayuda sobre un addon específico:

```text
rtg help <comando>
```

Para consultar sus idiomas:

```text
rtg help <comando> -lang
```
