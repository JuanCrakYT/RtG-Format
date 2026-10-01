RtG-CLI — Ayuda
================

RtG-CLI es la interfaz de línea de comandos del ecosistema RtG-Format.
Permite descubrir y ejecutar addons, consultar idiomas, ver reglas y versión.

Uso
-----

  rtg [OPCIONES] <COMANDO> [ARGUMENTOS]

  El primer argumento identifica el comando o addon a ejecutar.

  Ejemplos:
    rtg image
    rtg preview
    rtg help image


Comandos del sistema
---------------------

  -h, --help        Muestra esta ayuda general
  -v, --version     Muestra la versión de RtG-CLI
  -l, --lang        Lista los idiomas disponibles en RtG-CLI
  -r, --rules       Muestra las reglas de RtG-CLI
  -c, --commands    Lista los comandos internos de RtG-CLI
  -a, --addons      Lista los addons con documentación disponible
  -u, --usage       Muestra la información de uso común del sistema (nuevo)
  -u-<idioma>       Muestra el uso en un idioma específico (ej: -u-es, -u-en) (nuevo)
  --usage-<idioma>  Muestra el uso en un idioma específico (ej: --usage-es, --usage-en) (nuevo)
  -language <idioma>  Establece el idioma del texto de inicio (void)

Comando: help
--------------

  rtg help                    # Ayuda general (esta pantalla)
  rtg help <comando>          # Ayuda de un comando/addon específico
  rtg help <comando> -<idioma>  # Ayuda en idioma específico (ej: -es, -en)
  rtg help <comando> -lang      # Idiomas disponibles para ese comando
  rtg help -u                  # Uso común (nuevo)
  rtg help -u-<idioma>         # Uso en idioma específico (ej: -u-es) (nuevo)
  rtg help --usage             # Uso común (nuevo)
  rtg help --usage-<idioma>    # Uso en idioma específico (ej: --usage-es) (nuevo)
  rtg help usage               # Uso común (sintaxis alternativa, nuevo)

  Ejemplos:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es

Comando: version
-----------------

  rtg -v
  rtg --version

  Muestra la versión y el contenido de versión en todos los idiomas disponibles.


Comando: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<idioma>   # Reglas en idioma específico (ej: rtg -r -en)

  Por defecto usa el primer idioma definido en 'rules' (español).


Comando: lang
--------------

  rtg -l
  rtg --lang

  Lista todos los idiomas disponibles organizados por categoría:
  Version, Rules, Help, Void, y por cada addon.


Comando: commands
------------------

  rtg -c
  rtg --commands

  Lista exclusivamente los comandos internos de RtG-CLI.
  No incluye comandos de addons.


Comando: addons
----------------

  rtg -a
  rtg --addons

  Lista los addons que tienen documentación/ayuda visible para el usuario.
  Un addon registrado pero sin documentación no aparece aquí.


Comando: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<idioma>       # Uso en idioma específico (ej: -u-es, -u-en) (nuevo)
  --usage-<idioma>      # Uso en idioma específico (ej: --usage-es, --usage-en) (nuevo)

  Muestra la información de uso común del sistema (void) en el idioma solicitado.
  El idioma debe existir en 'void-language' de assets.json.


Comando: language
------------------

  rtg -language <idioma>

  Selecciona el idioma del texto de inicio (void).
  El idioma debe existir en 'void-language' de assets.json.

  Ejemplo:
    rtg -language en


Addons disponibles
-------------------

  image      | RtG Image        - Convertidor de imágenes
  preview    | RtG Preview      - Visor 3D de builds RtG-Format
  test-addon | RtG Test Addon   - Addon de prueba para validación


Idiomas
--------

Los idiomas se indican con un solo guion: -es, -en, -pt, etc.
El idioma no cambia el nombre interno del comando.

  rtg help image -es    # Ayuda en español
  rtg help image -en    # Ayuda en inglés
  rtg -r -en            # Reglas en inglés

  Para ver idiomas de un addon:
    rtg help image -lang

  El significado de -lang depende de su posición:
    rtg --lang          # Idiomas de RtG-CLI (antes del addon)
    rtg image -lang     # Idiomas del addon (después del addon)


Argumentos de addons
---------------------

Después de identificar un addon, los argumentos se clasifican por prefijo:

  sin guion       -> addon        (ej: convert, archivo.png)
  --opcion        -> addon        (ej: --width 128)
  -opcion         -> RtG-CLI      (ej: -lang, -en)

Ejemplos:
  rtg image convert archivo.png     # convert, archivo.png -> addon
  rtg image --width 128             # --width 128 -> addon
  rtg image -lang                   # -lang -> RtG-CLI (idiomas del addon)
  rtg image -en                     # -en -> RtG-CLI (selector de idioma)


Argumentos con espacios
------------------------

Los argumentos con espacios deben ir entre comillas:

  rtg image "mi imagen.png" "salida.json"

RtG-CLI conserva el orden y pasa los argumentos tal cual al addon.


Más información
----------------

  rtg help <comando>      # Ayuda detallada de un addon
  rtg help <comando> -lang  # Idiomas de ese addon
  rtg --addons            # Ver todos los addons documentados
  rtg --commands          # Ver comandos internos