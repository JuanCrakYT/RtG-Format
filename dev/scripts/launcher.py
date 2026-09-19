import subprocess
import sys
from pathlib import Path

import pygame


# dev/scripts/
BASE_DIR = Path(__file__).resolve().parent

# Herramientas disponibles
TOOLS = [
    {
        "name": "Organize Polaroid",
        "script": BASE_DIR.parent / "organize_polaroid.py",
    },
    {
        "name": "Extract Texture IDs",
        "script": BASE_DIR / "textures" / "TextureId.py",
    },
    {
        "name": "Open Texture IDs",
        "script": BASE_DIR / "textures" / "openTexturesID.py",
    },
    {
        "name": "Open Asset IDs",
        "script": BASE_DIR / "openAssetID.py",
    },
]


# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────

WIDTH = 800
HEIGHT = 600

FPS = 60

BUTTON_WIDTH = 500
BUTTON_HEIGHT = 55
BUTTON_GAP = 15

FONT_SIZE = 26
TITLE_SIZE = 38
STATUS_SIZE = 20


def run_tool(tool):
    """Ejecuta una herramienta Python."""

    script = Path(tool["script"])

    if not script.exists():
        return f"ERROR: No se encontró {script}"

    try:
        subprocess.Popen(
            [sys.executable, str(script)],
            cwd=script.parent,
        )

        return f"Ejecutando: {tool['name']}"

    except Exception as error:
        return f"ERROR: {error}"


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PolaroidPhoto Tools")

    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, TITLE_SIZE)
    button_font = pygame.font.Font(None, FONT_SIZE)
    status_font = pygame.font.Font(None, STATUS_SIZE)

    running = True
    status = "Ready"

    buttons = []

    total_height = (
        len(TOOLS) * BUTTON_HEIGHT
        + (len(TOOLS) - 1) * BUTTON_GAP
    )

    start_y = 150

    for index, tool in enumerate(TOOLS):
        x = (WIDTH - BUTTON_WIDTH) // 2
        y = start_y + index * (BUTTON_HEIGHT + BUTTON_GAP)

        rect = pygame.Rect(
            x,
            y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )

        buttons.append((rect, tool))

    while running:
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect, tool in buttons:
                        if rect.collidepoint(mouse_position):
                            status = run_tool(tool)

        screen.fill((25, 25, 25))

        # Título
        title = title_font.render(
            "PolaroidPhoto Tools",
            True,
            (240, 240, 240),
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, 70)
        )

        screen.blit(title, title_rect)

        # Botones
        for rect, tool in buttons:
            hovered = rect.collidepoint(mouse_position)

            if hovered:
                background = (70, 70, 70)
            else:
                background = (45, 45, 45)

            pygame.draw.rect(
                screen,
                background,
                rect,
                border_radius=8,
            )

            pygame.draw.rect(
                screen,
                (100, 100, 100),
                rect,
                width=2,
                border_radius=8,
            )

            text = button_font.render(
                tool["name"],
                True,
                (235, 235, 235),
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            screen.blit(text, text_rect)

        # Estado
        status_text = status_font.render(
            f"Status: {status}",
            True,
            (180, 180, 180),
        )

        status_rect = status_text.get_rect(
            center=(WIDTH // 2, HEIGHT - 40)
        )

        screen.blit(status_text, status_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
