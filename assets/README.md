# Assets

This directory contains the visual assets used by **RtG-Format**, including project branding, logos, banners, and documentation images.

## Directory Structure

```tree
assets/
├── images/
│   ├── banner.jpeg
│   ├── banner.png
│   ├── banner.svg
│   └── logo/
│       ├── RtG-Format.svg
│       ├── RtG-Format.png
│       ├── RtG-Format-Shape.svg
│       ├── RtG-Format-Background.svg
│       ├── official-banners/
│       │   ├── RtG-1.webp
│       │   ├── RtG-2.webp
│       │   ├── RtG-3.webp
│       │   ├── RtG-4.webp
│       │   └── RtG-5.webp
│       └── versions/
│           └── v1/
│               ├── RtG-Format-v1.svg
│               └── RtG-Format-v1.png
```

## Images

The [`images/`](images/) directory contains visual resources used throughout the repository.

### Banners

The root-level banner files are general project banner assets:

* [`banner.svg`](images/banner.svg) — SVG banner asset.
* [`banner.png`](images/banner.png) — PNG version of the banner.
* [`banner.jpeg`](images/banner.jpeg) — JPEG version of the banner.

### Current RtG-Format Logo

The current project logo is maintained in [`images/logo/`](images/logo/).

* [`RtG-Format.svg`](images/logo/RtG-Format.svg) — Main vector version of the RtG-Format logo.
* [`RtG-Format.png`](images/logo/RtG-Format.png) — Raster version of the RtG-Format logo.
* [`RtG-Format-Shape.svg`](images/logo/RtG-Format-Shape.svg) — Logo shape/isotype without the full wordmark.
* [`RtG-Format-Background.svg`](images/logo/RtG-Format-Background.svg) — Extended logo/banner artwork with its background.

These files represent the current project branding.

### Official RtG Banners

[`images/logo/official-banners/`](images/logo/official-banners/) contains the Road To Gramby's banner images used as backgrounds or visual references for project presentation.

The files are numbered for convenience:

* [`RtG-1.webp`](images/logo/official-banners/RtG-1.webp)
* [`RtG-2.webp`](images/logo/official-banners/RtG-2.webp)
* [`RtG-3.webp`](images/logo/official-banners/RtG-3.webp)
* [`RtG-4.webp`](images/logo/official-banners/RtG-4.webp)
* [`RtG-5.webp`](images/logo/official-banners/RtG-5.webp)

The `RtG-#` naming scheme allows additional banner variations to be added without changing the organization of the directory.

### Historical Logo Versions

[`images/logo/versions/`](images/logo/versions/) contains older logo versions preserved for historical reference.

The current historical version is stored under [`images/logo/versions/v1/`](images/logo/versions/v1/):

* [`RtG-Format-v1.svg`](images/logo/versions/v1/RtG-Format-v1.svg)
* [`RtG-Format-v1.png`](images/logo/versions/v1/RtG-Format-v1.png)

These files are **obsolete** and should not be used for new project materials or branding.

## Asset Guidelines

When adding or modifying project assets:

* Keep visual assets inside [`images/`](images/).
* Keep current RtG-Format branding inside [`images/logo/`](images/logo/).
* Keep official Road To Gramby's banner references inside [`images/logo/official-banners/`](images/logo/official-banners/).
* Keep obsolete logo versions inside [`images/logo/versions/`](images/logo/versions/).
* Do not use files under `versions/` as current branding.
* Prefer SVG for logos and other graphics that need to scale cleanly.
* Use PNG or JPEG when a raster format is specifically required.
* Use WebP for the official banner images stored in `official-banners/`.
* When replacing an asset, preserve older versions when they are useful for historical reference instead of silently overwriting them.

## Related Documentation

* [`../README.md`](../README.md) — Main project documentation.
* [`../structure.md`](../structure.md) — Repository structure.
* [`images/`](images/) — Image assets not directly used by the project page.
