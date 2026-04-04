# Bhagamandala Heritage House — 3D Interactive Plan

> An interactive 3D architectural walkthrough of a traditional **Kodagu Gowda Ainmane**-inspired residence,
> built with Three.js. Includes multilingual documentation, automated plan generation, and a full build pipeline.

[![Live 3D Viewer](https://img.shields.io/badge/3D_Viewer-Launch-c4956a?style=for-the-badge&logo=three.js)](3d-viewer/index.html)

---

## Overview

A **G+1 residential house** designed for Bhagamandala–Talakaveri Road, Kodagu (Coorg), Karnataka.
The design combines traditional Kodagu heritage architecture with modern amenities.

| Spec | Detail |
|------|--------|
| **Plot** | 60 × 50 ft, East-facing |
| **Building** | 42 × 38 ft (including 42 × 8 veranda) |
| **Built-up** | ~2,909 sqft (G+1) |
| **Style** | Kodagu Gowda Ainmane heritage |
| **Vastu** | Compliant — East entrance, NE Pooja |

## Key Features

- **Exposed Laterite Walls** (ಜಂಬಿಟ್ ಕಲ್ಲು) — Bedrooms feature traditional laterite stone sealed with linseed oil. No plaster, no paint.
- **Ainmane Veranda (Jagali)** — 42 × 8 ft front veranda with 5 teak wood pillars, Kota stone flooring, and wooden swing.
- **Interactive 3D Walkthrough** — WebGL-powered viewer with orbit controls, room details, X-ray mode, exploded view, day/night toggle.
- **Multilingual Plans** — Documentation in English, Kannada (ಕನ್ನಡ), and Malayalam (മലയാളം).
- **Automated Pipeline** — Python scripts to regenerate floor plans, elevation images, PDFs, and sync the 3D model.
- **Mangalore Tile Roof** — Traditional half-round clay tiles with hip-and-gable profile.

## 3D Viewer

Open [`3d-viewer/index.html`](3d-viewer/index.html) in a browser (serve via any HTTP server):

```bash
# Python
python -m http.server 8899 -d 3d-viewer

# Node
npx serve 3d-viewer -p 8899
```

### Controls

| Input | Action |
|-------|--------|
| Drag | Orbit camera |
| Scroll | Zoom |
| Shift+Drag | Pan |
| Click room | Show details |
| `R` | Reset camera |
| `E` | Explode view |
| `X` | X-ray walls |
| `N` | Night mode |

### Viewer Features

- **Floor filter** — View Ground Floor, First Floor, Site, or All
- **Camera presets** — Bird's Eye, Front, Inside GF, Sitout
- **Room panel** — Lists all 18 rooms with dimensions, click to fly-to
- **Detail card** — Wall finish, flooring, Vastu direction, features per room
- **Heritage highlight** — Laterite-tagged rooms with Kodagu heritage badge

## Room Layout

### Ground Floor (11 rooms)

| Room | Size | Wall Finish | Flooring |
|------|------|-------------|----------|
| Hall / Living | 16 × 16 | Plastered — AP Marshmallow | Beige vitrified |
| Master Bedroom | 16 × 16 | **Exposed Laterite + Linseed Oil** | Beige vitrified |
| Bedroom 2 (Guest) | 14 × 14 | **Exposed Laterite + Linseed Oil** | Beige vitrified |
| Kitchen | 16 × 14 | Plastered — AP Buttercup | Anti-skid ceramic |
| Store Room | 10 × 8 | Plastered — White | Cement / Kota |
| Bath 1 (Master) | 10 × 7 | Ceramic tiles to 7′ | Anti-skid ceramic |
| Bath 2 (BR2) | 10 × 7 | Ceramic tiles to 7′ | Anti-skid ceramic |
| Passage | 10 × 3 | White | Vitrified |
| Staircase | 10 × 5 | White | Granite steps |
| Veranda / Jagali | 42 × 8 | Open — 5 wood pillars | Kota Stone |
| Guest WC | 4 × 4 | Ceramic tiles | Anti-skid |

### First Floor (7 rooms)

| Room | Size | Wall Finish | Flooring |
|------|------|-------------|----------|
| FF Master Bedroom | 16 × 16 | **Exposed Laterite + Linseed Oil** | Beige vitrified |
| Family Hall / TV | 16 × 14 | Plastered — AP Marshmallow | Beige vitrified |
| Work Room / Study | 10 × 14 | Plastered — AP Ivory Spark | Beige vitrified |
| Bath 3 (FF Master) | 10 × 7 | Ceramic tiles to 7′ | Anti-skid ceramic |
| Landing + Passage | 10 × 4 | White | Vitrified |
| Staircase (FF) | 10 × 5 | White | Granite steps |
| Covered Sitout | 26 × 8 | Open — MS grill screen | Anti-skid tiles |

## Materials

| Material | Application | Source |
|----------|-------------|--------|
| **Laterite Stone** (ಜಂಬಿಟ್ ಕಲ್ಲು) | Bedroom walls — exposed, sealed with linseed oil | Local quarry, Kodagu |
| **Mangalore Tiles** | Roof — half-round clay tiles | Mangalore / Udupi |
| **Kota Stone** | Veranda / Jagali flooring | Rajasthan |
| **Teak Wood** | Veranda pillars, doors, window frames | Kerala / Karnataka |
| **Granite** | Steps, bathroom basins | Local |
| **Vitrified Tiles** (beige) | Main rooms flooring | Standard |
| **Anti-skid Ceramic** | Kitchen and bathroom flooring | Standard |
| **MS Grill** | First floor sitout railing + window grills | Local fabrication |

## Design Heritage

This house draws from the **Kodagu Gowda Ainmane** tradition:

- **Laterite Construction** — The signature red-brown laterite stone, locally called *ಜಂಬಿಟ್ ಕಲ್ಲು* (jambitt kallu), is used as an exposed wall finish in bedrooms. Sealed with linseed oil for durability and a warm natural glow.
- **Veranda / Jagali** — Traditional sitting area at the front of every Ainmane. 42 ft wide with 5 teak pillars.
- **Mangalore Tile Roof** — Classic hip-and-gable roof with clay tiles, visible from the road.
- **Coffee Estate Backdrop** — First floor sitout designed for views of the surrounding coffee estate and Western Ghats.

## Build Pipeline

The automated pipeline regenerates all outputs from source:

```bash
# Install dependencies
pip install Pillow fpdf2 matplotlib

# Run full pipeline
python pipeline.py --all

# Individual steps
python generate_plans_v4.py    # 6 architectural plan images
python generate_pdfs.py         # 5 PDFs (EN, KN, ML, Cost, Images)
```

Pipeline steps: **Images → PDFs → 3D Sync → Context Update**

## Project Structure

```
├── 3d-viewer/
│   ├── index.html          # Interactive 3D walkthrough (Three.js)
│   └── index_v1.html       # Version 1 backup
├── *_v4.png                # v4 plan images (GF, FF, Front, Back, Roof, Site)
├── *_v4.md                 # v4 documentation (EN, KN, ML)
├── *_v4.pdf                # v4 PDFs
├── generate_plans_v4.py    # Image generator (PIL/matplotlib)
├── generate_pdfs.py        # PDF generator (fpdf2)
├── pipeline.py             # Automation pipeline
└── README.md
```

## Tech Stack

- **Three.js** r0.164.1 — WebGL 3D rendering, PBR materials, procedural canvas textures
- **Python** — PIL/Pillow for plan images, fpdf2 for PDFs, matplotlib for charts
- **Vanilla HTML/CSS/JS** — Single-file 3D viewer, no build tools needed

## License

This project is personal/educational. The architectural design is for a specific plot in Kodagu, Karnataka.

---

*Kodagu (Coorg) • Karnataka • India*
