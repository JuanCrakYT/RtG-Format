# ============================================================
# RtG-CLI Release Script
# ============================================================
#
# Uso:
#   .\release.ps1 0.4.1
#
# También acepta:
#   .\release.ps1 v0.4.1
#
# El script:
#   1. Comprueba Git y GitHub CLI
#   2. Comprueba autenticación de GitHub
#   3. Comprueba que estamos en el repositorio correcto
#   4. Comprueba el estado de Git
#   5. Comprueba que la versión no exista
#   6. Crea un tag anotado
#   7. Sube el tag a GitHub
#   8. Crea el GitHub Release
#
# ============================================================

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $RepoRoot

# ------------------------------------------------------------
# FUNCIONES
# ------------------------------------------------------------

function Fail {
    param (
        [string]$Message
    )

    Write-Host ""
    Write-Host "ERROR: $Message" -ForegroundColor Red
    Write-Host ""

    exit 1
}

function Step {
    param (
        [string]$Number,
        [string]$Message
    )

    Write-Host ""
    Write-Host "[$Number] $Message" -ForegroundColor Yellow
}

# ------------------------------------------------------------
# BANNER
# ------------------------------------------------------------

Clear-Host

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "                 RtG-CLI RELEASE                 " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# VERSION
# ------------------------------------------------------------

$Version = $args[0]

if (-not $Version) {
    $Version = Read-Host "Version (ejemplo: 0.4.1)"
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    Fail "No se especificó una versión."
}

# Permitir tanto 0.4.1 como v0.4.1
$Version = $Version.Trim()

if ($Version.StartsWith("v")) {
    $Version = $Version.Substring(1)
}

# Validar formato semver básico
if ($Version -notmatch '^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$') {
    Fail "La versión '$Version' no tiene un formato válido. Usa algo como 0.4.1"
}

$Tag = "v$Version"

Write-Host "Versión : $Version" -ForegroundColor White
Write-Host "Tag     : $Tag" -ForegroundColor White
Write-Host "Ruta    : $RepoRoot" -ForegroundColor White

# ------------------------------------------------------------
# 1. COMPROBAR PROGRAMAS
# ------------------------------------------------------------

Step "1/8" "Comprobando programas necesarios..."

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Fail "Git no está instalado o no está en PATH."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Fail "GitHub CLI (gh) no está instalado.`nInstálalo con:`nwinget install --id GitHub.cli"
}

Write-Host "Git .............. OK" -ForegroundColor Green
Write-Host "GitHub CLI ....... OK" -ForegroundColor Green

# ------------------------------------------------------------
# 2. AUTENTICACIÓN
# ------------------------------------------------------------

Step "2/8" "Comprobando autenticación de GitHub..."

gh auth status

if ($LASTEXITCODE -ne 0) {
    Fail "GitHub CLI no está autenticado.`nEjecuta:`ngh auth login"
}

Write-Host "GitHub ........... autenticado" -ForegroundColor Green

# ------------------------------------------------------------
# 3. REPOSITORIO
# ------------------------------------------------------------

Step "3/8" "Comprobando repositorio Git..."

$IsGitRepo = git rev-parse --is-inside-work-tree 2>$null

if ($IsGitRepo -ne "true") {
    Fail "La carpeta actual no pertenece a un repositorio Git."
}

$Remote = git remote get-url origin 2>$null

if (-not $Remote) {
    Fail "El repositorio no tiene un remote 'origin'."
}

$CurrentBranch = git branch --show-current

Write-Host "Branch ........... $CurrentBranch" -ForegroundColor White
Write-Host "Origin ........... $Remote" -ForegroundColor White

# ------------------------------------------------------------
# 4. ESTADO DE GIT
# ------------------------------------------------------------

Step "4/8" "Comprobando estado de Git..."

$Status = git status --porcelain

if ($Status) {

    Write-Host ""
    Write-Host "Hay cambios sin commit:" -ForegroundColor Yellow
    Write-Host ""

    git status --short

    Write-Host ""

    $Continue = Read-Host "¿Quieres continuar de todos modos? (y/N)"

    if ($Continue -ne "y" -and $Continue -ne "Y") {
        Fail "Release cancelado porque existen cambios sin commit."
    }
}
else {
    Write-Host "Working tree limpio." -ForegroundColor Green
}

# ------------------------------------------------------------
# 5. COMPROBAR TAG
# ------------------------------------------------------------

Step "5/8" "Comprobando si el tag ya existe..."

$LocalTag = git tag --list $Tag

if ($LocalTag) {
    Fail "El tag '$Tag' ya existe localmente. Debes utilizar otra versión."
}

$RemoteTag = git ls-remote --tags origin "refs/tags/$Tag"

if ($RemoteTag) {
    Fail "El tag '$Tag' ya existe en GitHub. Debes utilizar otra versión."
}

Write-Host "Tag disponible: $Tag" -ForegroundColor Green

# ------------------------------------------------------------
# INFORMACIÓN DEL COMMIT
# ------------------------------------------------------------

$CommitHash = git rev-parse HEAD

$CommitShort = git rev-parse --short HEAD

Write-Host ""
Write-Host "Commit actual: $CommitShort" -ForegroundColor White

# ------------------------------------------------------------
# CONFIRMACIÓN
# ------------------------------------------------------------

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Se va a crear el siguiente release:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   RtG-CLI $Tag" -ForegroundColor White
Write-Host ""
Write-Host "   Commit: $CommitHash" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$Confirm = Read-Host "¿Continuar? (y/N)"

if ($Confirm -ne "y" -and $Confirm -ne "Y") {
    Write-Host ""
    Write-Host "Release cancelado." -ForegroundColor Yellow
    exit 0
}

# ------------------------------------------------------------
# 6. CREAR TAG
# ------------------------------------------------------------

Step "6/8" "Creando tag $Tag..."

git tag -a $Tag -m "RtG-CLI $Tag"

if ($LASTEXITCODE -ne 0) {
    Fail "No se pudo crear el tag."
}

Write-Host "Tag creado." -ForegroundColor Green

# ------------------------------------------------------------
# SUBIR TAG
# ------------------------------------------------------------

Write-Host ""
Write-Host "Subiendo tag a GitHub..." -ForegroundColor Yellow

git push origin $Tag

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "Falló la subida del tag." -ForegroundColor Red
    Write-Host "El tag local '$Tag' todavía existe." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Puedes volver a intentar con:" -ForegroundColor Yellow
    Write-Host "git push origin $Tag" -ForegroundColor White

    exit 1
}

Write-Host "Tag subido correctamente." -ForegroundColor Green

# ------------------------------------------------------------
# 7. CREAR RELEASE
# ------------------------------------------------------------

Step "7/8" "Creando GitHub Release..."

$Notes = @"
# RtG-CLI $Tag

Release de RtG-CLI.

## Versión

$Version

## Commit

$CommitHash

## Cambios

Consulta el historial de commits de GitHub para ver todos los cambios incluidos en esta versión.
"@

gh release create $Tag `
    --title "RtG-CLI $Tag" `
    --notes $Notes

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "No se pudo crear el GitHub Release." -ForegroundColor Red
    Write-Host ""
    Write-Host "El tag '$Tag' ya fue creado y subido." -ForegroundColor Yellow
    Write-Host "Puedes crear el release manualmente desde GitHub." -ForegroundColor Yellow
    Write-Host ""

    exit 1
}

# ------------------------------------------------------------
# 8. MOSTRAR RESULTADO
# ------------------------------------------------------------

Step "8/8" "Obteniendo información del release..."

$ReleaseUrl = gh release view $Tag --json url --jq ".url"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "             RELEASE CREADO CORRECTAMENTE         " -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Versión : $Version" -ForegroundColor White
Write-Host "Tag     : $Tag" -ForegroundColor White
Write-Host "Commit  : $CommitShort" -ForegroundColor White
Write-Host ""

Write-Host "Release:" -ForegroundColor Cyan
Write-Host $ReleaseUrl -ForegroundColor White
Write-Host ""

Write-Host "==================================================" -ForegroundColor Green
Write-Host ""