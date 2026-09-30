# RtG-CLI

CLI oficial del ecosistema **RtG-Format**.

> **Estado:** ✅ Reconstrucción completada  
> **Versión:** 1.2.0  
> **Fecha:** 2026-09-30

---

## 1. Propósito

**RtG-CLI** es la interfaz de línea de comandos del ecosistema RtG-Format.

Su función es proporcionar una interfaz común para:

- consultar información de RtG-Format;
- mostrar ayuda y reglas;
- administrar idiomas (19 soportados);
- descubrir y ejecutar addons (3 disponibles);
- ejecutar comandos auxiliares del ecosistema;
- gestionar versiones;
- proporcionar una base estable para herramientas futuras;
- servir como punto de integración para **RtG-Language**.

RtG-CLI es una herramienta formal, modular, testeada y mantenible.

---

## 2. Inicio rápido

```bash
# Desde el directorio RtG-CLI
python rtg.py

# O en Windows
rtg.cmd
```

### Comandos básicos

```bash
rtg                    # Muestra texto de inicio (void)
rtg -h                 # Ayuda general
rtg -v                 # Versión
rtg -l                 # Idiomas disponibles
rtg -r                 # Reglas (español por defecto)
rtg -c                 # Comandos internos
rtg -a                 # Addons documentados
rtg help               # Ayuda general
rtg help image         # Ayuda del addon image
rtg help image -en     # Ayuda en inglés
rtg help image -lang   # Idiomas del addon image
rtg image              # Info del addon image
rtg image convert      # Ejecuta comando del addon
rtg test-addon echo "hola"  # Addon de prueba
```

---

## 3. Arquitectura

```
RtG-CLI/
├── rtg.py              # Entry point delgado
├── rtg.cmd             # Launcher Windows
├── assets.json         # Configuración completa (19 idiomas)
├── schemas/
│   └── assets.schema.json  # Schema JSON para validación
├── rtg_cli/            # Núcleo modular
│   ├── __init__.py
│   ├── application.py  # Orquestador principal
│   ├── arguments.py    # Parser formal de argumentos
│   ├── configuration.py # Carga y validación assets.json
│   ├── addons.py       # Registro y descubrimiento de addons
│   ├── execution.py    # Ejecución de comandos internos y addons
│   ├── languages.py    # Gestión de 19 idiomas
│   ├── diagnostics.py  # Errores estructurados + exit codes
│   ├── help.py         # Sistema de ayuda externa
│   └── version.py      # Gestión de versiones
├── en/ .. hu/          # 19 directorios de idioma (rules, help, void)
├── test_addon/         # Addon de prueba real
│   └── commands.py     # Interface Python (echo, fail, stdout, stderr, exit-code)
├── tests/              # Tests automatizados
│   ├── arguments/
│   ├── commands/
│   ├── addons/
│   ├── execution/
│   ├── languages/
│   ├── configuration/
│   ├── errors/
│   └── integration/
└── docs/               # Documentación técnica
    ├── ARCHITECTURE.md
    ├── COMMANDS.md
    ├── ADDONS.md
    ├── PROGRAM-COMMANDS.md
    ├── ARGUMENTS.md
    ├── LANGUAGES.md
    ├── CONFIGURATION.md
    ├── ERRORS.md
    └── INTEGRATION.md
```

---

## 4. Idiomas soportados (19)

| Código | Nombre | Origen |
|--------|--------|--------|
| es | Español | RtG-AI |
| en | English | RtG-AI |
| pt | Português | RtG-AI |
| de | Deutsch | RtG-AI |
| fr | Français | RtG-AI |
| ru | Русский | RtG-AI |
| zh | 中文 | RtG-AI |
| ja | 日本語 | RtG-AI |
| ko | 한국어 | RtG-AI |
| it | Italiano | RtG-AI |
| tr | Türkçe | RtG-AI |
| pl | Polski | RtG-AI |
| zh-TW | 繁體中文 | Adicional |
| ar | العربية | Adicional |
| hi | हिन्दी | Adicional |
| nl | Nederlands | Adicional |
| sv | Svenska | Adicional |
| cs | Čeština | Adicional |
| hu | Magyar | Adicional |

**12 idiomas de RtG-AI + 7 adicionales = 19 total**

---

## 5. Addons disponibles

| ID | Nombre | Descripción | Idiomas | Interface |
|----|--------|-------------|---------|-----------|
| `image` | RtG Image | Conversor de imágenes | 19 | Python (`../tools/RtG Image/commands.py`) |
| `preview` | RtG Preview | Visor 3D builds RtG | 19 | JavaScript (`../RtG-Preview/commands.js`) |
| `test-addon` | RtG Test Addon | Validación CLI | 2 (es, en) | Python (`test_addon/commands.py`) |

### Distinción clave
- **Registered addon**: Existe en `assets.json` → 3 addons
- **Documented/User-visible addon**: Tiene `lang` array o `internal.help` → 3 addons (todos documentados)

---

## 6. Contrato de Program Commands

### Interface Python
```python
def execute(args: list[str]) -> int:      # Requerido
def get_commands() -> list[str]:          # Opcional
def get_help(command: str, lang: str) -> str | None:  # Opcional
```

### Interface JavaScript (Node.js)
```javascript
// execute(args), get_commands(), get_help(command, lang)
// Ejecutado via: node script.js [args]
```

### Flujo de ejecución
```
rtg <addon> [args]
    ↓
AddonExecutor
    ↓
ProgramCommandInterface (Python/JS)
    ↓
execute(args) → exit_code
stdout/stderr propagados
```

### Propiedades clave
- Argumentos preservados en orden original
- `--` y sin prefijo → addon
- `-` → RtG-CLI (ej: `-lang`, `-en`)
- Exit codes: 0=éxito, 1=error uso, 2=comando desconocido, 5=addon no encontrado, 7=fallo ejecución addon, etc.

---

## 7. Sistema de Argumentos

### Ownership rules (después de identificar addon)
| Prefijo | Dueño | Ejemplos |
|---------|-------|----------|
| (ninguno) | Addon | `convert`, `archivo.png` |
| `--` | Addon | `--width 128`, `--output` |
| `-` | RtG-CLI | `-lang`, `-en` |

### Opciones del sistema (antes del addon)
- `-v, --version`
- `-h, --help`
- `-l, --lang`
- `-r, --rules`
- `-c, --commands`
- `-a, --addons`
- `-language <idioma>`

### Selectores de idioma
- `-es`, `-en`, `-pt`, etc. (un solo guion)
- `-language en` (solo antes del addon, para void text)

---

## 8. Tests

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# O usar unittest
python -m unittest discover -s tests -v
```

### Cobertura
- ✅ `tests/arguments/` - Parser de argumentos
- ✅ `tests/commands/` - Comandos internos (help, version, rules, lang, commands, addons, language)
- ✅ `tests/addons/` - Registro y descubrimiento
- ✅ `tests/execution/` - Ejecución addons (stdout, stderr, exit codes)
- ✅ `tests/languages/` - 19 idiomas, fallback, validación
- ✅ `tests/configuration/` - Carga assets.json, schema
- ✅ `tests/errors/` - Diagnostics, exit codes
- ✅ `tests/integration/` - CLI completa via subprocess

---

## 9. Validación manual

```bash
# Comandos básicos
python rtg.py
python rtg.py -h
python rtg.py -v
python rtg.py -l
python rtg.py -r
python rtg.py -c
python rtg.py -a

# Help
python rtg.py help
python rtg.py help image
python rtg.py help image -en
python rtg.py help image -lang

# Addons
python rtg.py image
python rtg.py preview
python rtg.py test-addon
python rtg.py test-addon echo "hola mundo"
python rtg.py test-addon fail "error"
python rtg.py test-addon exit-code 42
python rtg.py test-addon -lang

# Errores
python rtg.py unknowncmd
python rtg.py --invalid-option
```

---

## 10. Documentación

| Archivo | Descripción |
|---------|-------------|
| `docs/ARCHITECTURE.md` | Arquitectura modular, diagrama componentes, flujo datos |
| `docs/COMMANDS.md` | Referencia completa de comandos |
| `docs/ADDONS.md` | Especificación formal de addons |
| `docs/PROGRAM-COMMANDS.md` | Contrato de ejecución (Python/JS) |
| `docs/ARGUMENTS.md` | Parser formal, ownership rules |
| `docs/LANGUAGES.md` | 19 idiomas, códigos, nombres, fallback |
| `docs/CONFIGURATION.md` | assets.json, schema, campos |
| `docs/ERRORS.md` | Categorías error, exit codes |
| `docs/INTEGRATION.md` | Integración RtG-Language, API externa |

---

## 11. Integración futura: RtG-Language

RtG-CLI provee interfaz estable para futura integración:

```text
rtg build archivo.rtg     # Futuro comando
rtg validate archivo.json # Futuro comando
```

**No se implementa RtG-Language aquí** — solo la interfaz de integración:
- `ProgramCommandInterface` abstracta
- Addon registry con metadata de versión/compatibilidad
- Configuración versionada en assets.json
- Error handling estructurado

---

## 12. RtG-Preview

El addon `preview` usa **RtG-Preview legacy** (rama main de RtG-Format).
- Estado: **Legacy/Deprecated** para rama moderna PolaroidPhoto/RtG
- Interface: JavaScript via Node.js
- No integrar en RtG-Language moderno
- Decisión documentada en `docs/ADDONS.md`

---

## 13. Estado de completación

✅ **Completado:**
- Arquitectura modular (`rtg_cli/`)
- Entry point delgado (`rtg.py`)
- 19 idiomas con rules/help/void completos
- 3 addons (image, preview, test-addon)
- test-addon ejecutable real (stdout/stderr/exit codes)
- Parser formal argumentos
- Diagnostics estructurados + exit codes
- Schema JSON (assets.schema.json)
- Tests automatizados (8 categorías)
- Documentación técnica (9 archivos)
- Validación manual exitosa

📋 **Pendiente menor:**
- CI/CD pipeline (GitHub Actions)
- Más addons de producción (RtG Image commands.py real)

---

## 14. Licencia

MIT License — Ver `LICENSE` en raíz del repo.