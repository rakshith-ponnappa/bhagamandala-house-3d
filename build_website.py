#!/usr/bin/env python3
"""Generate the Bhagamandala House website — landing page + enhanced 3D viewer."""
import os, shutil

DOCS = os.path.join(os.path.dirname(__file__), "docs")
VIEWER_SRC = os.path.join(os.path.dirname(__file__), "3d-viewer", "index.html")
os.makedirs(DOCS, exist_ok=True)

# Copy plan images into docs/img/
IMG_DIR = os.path.join(DOCS, "img")
os.makedirs(IMG_DIR, exist_ok=True)
for f in ["GF_Plan_v4.png", "FF_Plan_v4.png", "Front_Elevation_v4.png",
          "Back_Elevation_v4.png", "Roof_Solar_v4.png", "Site_Layout_v4.png"]:
    src = os.path.join(os.path.dirname(__file__), f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(IMG_DIR, f))

# ─── LANDING PAGE ───────────────────────────────────────────────────────
LANDING = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bhagamandala Heritage House — Kodagu, Karnataka</title>
<meta name="description" content="Interactive 3D walkthrough of a traditional Kodagu Gowda Ainmane heritage house. Explore rooms, materials, and floor plans.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--gold:#c4956a;--gold-light:#d4a87a;--dark:#0a0a0a;--card:#111114;--text:#c8c8c8;--muted:#666;--radius:12px}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--dark);color:var(--text);font-family:'Inter',system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
::selection{background:var(--gold);color:#000}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;height:64px;background:rgba(10,10,10,0.85);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,0.04);display:flex;align-items:center;justify-content:space-between;padding:0 clamp(20px,4vw,60px);z-index:100;transition:background .3s}
nav.scrolled{background:rgba(10,10,10,0.96)}
.nav-logo{font-family:'Playfair Display',serif;font-size:18px;font-weight:600;color:var(--gold);letter-spacing:.5px}
.nav-logo span{color:#555;font-weight:400;font-size:12px;margin-left:6px}
.nav-links{display:flex;gap:28px;align-items:center}
.nav-links a{color:var(--muted);text-decoration:none;font-size:13px;font-weight:500;transition:color .2s;letter-spacing:.3px}
.nav-links a:hover{color:var(--gold)}
.nav-cta{background:var(--gold)!important;color:#0a0a0a!important;padding:8px 20px;border-radius:6px;font-weight:600;font-size:12px!important;letter-spacing:.5px;transition:all .2s}
.nav-cta:hover{background:var(--gold-light)!important;transform:translateY(-1px)}

/* HERO */
.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px clamp(20px,5vw,80px) 40px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(196,149,106,0.06) 0%,transparent 60%),radial-gradient(ellipse at 70% 30%,rgba(100,80,60,0.04) 0%,transparent 50%)}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(196,149,106,0.08);border:1px solid rgba(196,149,106,0.15);color:var(--gold);padding:6px 16px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:24px}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(36px,6vw,72px);font-weight:700;color:#f0ece4;line-height:1.1;margin-bottom:16px;max-width:800px}
.hero h1 em{font-style:normal;color:var(--gold)}
.hero p{font-size:clamp(15px,1.8vw,19px);color:#888;max-width:600px;margin-bottom:36px;font-weight:300;line-height:1.7}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
.btn-primary{background:var(--gold);color:#0a0a0a;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;letter-spacing:.3px;transition:all .25s;display:inline-flex;align-items:center;gap:8px}
.btn-primary:hover{background:var(--gold-light);transform:translateY(-2px);box-shadow:0 8px 30px rgba(196,149,106,0.2)}
.btn-secondary{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);color:#ccc;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:500;font-size:14px;transition:all .25s;display:inline-flex;align-items:center;gap:8px}
.btn-secondary:hover{background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.2);transform:translateY(-2px)}
.hero-stats{display:flex;gap:clamp(24px,5vw,60px);margin-top:60px;padding-top:40px;border-top:1px solid rgba(255,255,255,0.05)}
.hero-stat{text-align:center}
.hero-stat .val{font-family:'Playfair Display',serif;font-size:clamp(24px,3vw,36px);font-weight:700;color:var(--gold)}
.hero-stat .lbl{font-size:11px;color:#555;text-transform:uppercase;letter-spacing:1.2px;margin-top:4px}

/* SECTIONS */
section{padding:clamp(60px,10vw,120px) clamp(20px,5vw,80px)}
.section-label{display:inline-block;font-size:11px;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(28px,4vw,44px);font-weight:600;color:#eee;margin-bottom:16px;line-height:1.2}
.section-desc{font-size:16px;color:#777;max-width:600px;margin-bottom:48px;line-height:1.7}

/* ABOUT */
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;max-width:1200px;margin:0 auto}
.about-img{aspect-ratio:4/3;background:var(--card);border-radius:var(--radius);overflow:hidden;border:1px solid rgba(255,255,255,0.04);position:relative}
.about-img iframe{width:100%;height:100%;border:none}
.about-img .overlay{position:absolute;inset:0;background:linear-gradient(135deg,rgba(196,149,106,0.08),transparent);pointer-events:none}
.about-features{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:32px}
.feat{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:8px;padding:16px;transition:all .25s}
.feat:hover{border-color:rgba(196,149,106,0.2);transform:translateY(-2px)}
.feat-icon{font-size:20px;margin-bottom:8px}
.feat h4{font-size:13px;color:#ddd;font-weight:600;margin-bottom:4px}
.feat p{font-size:11px;color:#666;line-height:1.5}

/* GALLERY */
.gallery-section{background:rgba(255,255,255,0.01)}
.gallery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1200px;margin:0 auto}
.gallery-card{background:var(--card);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);overflow:hidden;cursor:pointer;transition:all .3s}
.gallery-card:hover{border-color:rgba(196,149,106,0.25);transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,0.4)}
.gallery-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;filter:brightness(0.9);transition:filter .3s}
.gallery-card:hover img{filter:brightness(1)}
.gallery-card .caption{padding:12px 16px}
.gallery-card .caption h4{font-size:13px;color:#ddd;font-weight:600}
.gallery-card .caption p{font-size:11px;color:#666;margin-top:2px}

/* SPECS */
.specs-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;max-width:1200px;margin:0 auto}
.spec-card{background:var(--card);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);padding:28px;transition:all .25s}
.spec-card:hover{border-color:rgba(196,149,106,0.15)}
.spec-card h3{font-family:'Playfair Display',serif;font-size:17px;color:var(--gold);margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.04)}
.spec-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.02)}
.spec-row:last-child{border:none}
.spec-row .k{font-size:13px;color:#888}
.spec-row .v{font-size:13px;color:#ddd;font-weight:500;text-align:right}

/* MATERIALS */
.materials-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;max-width:1200px;margin:0 auto}
.mat-card{background:var(--card);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);padding:24px;text-align:center;transition:all .25s}
.mat-card:hover{border-color:rgba(196,149,106,0.2);transform:translateY(-3px)}
.mat-swatch{width:60px;height:60px;border-radius:50%;margin:0 auto 14px;border:3px solid rgba(255,255,255,0.06)}
.mat-card h4{font-size:14px;color:#ddd;font-weight:600;margin-bottom:4px}
.mat-card .mat-use{font-size:11px;color:var(--gold);margin-bottom:6px}
.mat-card p{font-size:11px;color:#666;line-height:1.5}

/* HERITAGE */
.heritage{background:linear-gradient(135deg,rgba(196,149,106,0.04),rgba(100,60,30,0.02));border-top:1px solid rgba(196,149,106,0.08);border-bottom:1px solid rgba(196,149,106,0.08)}
.heritage-content{max-width:800px;margin:0 auto;text-align:center}
.heritage-content blockquote{font-family:'Playfair Display',serif;font-size:clamp(20px,3vw,28px);color:#d4c4b0;line-height:1.5;font-style:italic;margin-bottom:20px}
.heritage-content cite{font-size:13px;color:var(--gold);font-style:normal;letter-spacing:.5px}
.heritage-tags{display:flex;gap:10px;justify-content:center;margin-top:28px;flex-wrap:wrap}
.heritage-tag{background:rgba(196,149,106,0.08);border:1px solid rgba(196,149,106,0.15);color:var(--gold);padding:6px 14px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:.5px}

/* CTA */
.cta-section{text-align:center;padding:clamp(80px,12vw,160px) 20px}
.cta-section h2{font-family:'Playfair Display',serif;font-size:clamp(32px,5vw,52px);color:#f0ece4;margin-bottom:16px}
.cta-section p{font-size:17px;color:#777;margin-bottom:36px;max-width:500px;margin-left:auto;margin-right:auto}

/* FOOTER */
footer{border-top:1px solid rgba(255,255,255,0.04);padding:40px clamp(20px,5vw,80px);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px}
footer .copy{font-size:12px;color:#444}
footer .copy a{color:var(--gold);text-decoration:none}
footer .links{display:flex;gap:20px}
footer .links a{color:#555;text-decoration:none;font-size:12px;transition:color .2s}
footer .links a:hover{color:var(--gold)}

/* LIGHTBOX */
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,0.92);backdrop-filter:blur(20px);z-index:200;display:none;align-items:center;justify-content:center;cursor:zoom-out}
.lightbox.open{display:flex}
.lightbox img{max-width:90vw;max-height:85vh;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,0.6)}
.lightbox .close{position:absolute;top:20px;right:24px;color:#fff;font-size:28px;cursor:pointer;width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(255,255,255,0.08);transition:background .2s}
.lightbox .close:hover{background:rgba(255,255,255,0.15)}

/* SCROLLBAR */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(196,149,106,0.3);border-radius:3px}

/* RESPONSIVE */
@media(max-width:900px){
  .about-grid{grid-template-columns:1fr;gap:32px}
  .gallery-grid{grid-template-columns:1fr 1fr}
  .nav-links a:not(.nav-cta){display:none}
}
@media(max-width:600px){
  .gallery-grid{grid-template-columns:1fr}
  .hero-stats{flex-direction:column;gap:16px}
  .about-features{grid-template-columns:1fr}
}

/* ANIMATIONS */
.fade-up{opacity:0;transform:translateY(30px);transition:opacity .6s ease,transform .6s ease}
.fade-up.visible{opacity:1;transform:translateY(0)}
</style>
</head>
<body>

<nav id="nav">
  <div class="nav-logo">BHAGAMANDALA <span>Residence</span></div>
  <div class="nav-links">
    <a href="#about">About</a>
    <a href="#gallery">Plans</a>
    <a href="#specs">Specs</a>
    <a href="#materials">Materials</a>
    <a href="viewer.html" class="nav-cta">&#9654; 3D WALKTHROUGH</a>
  </div>
</nav>

<header class="hero">
  <div class="hero-badge">&#9670; Kodagu Gowda Ainmane Heritage</div>
  <h1>A Home Rooted in <em>Kodagu</em> Tradition</h1>
  <p>Interactive 3D architectural walkthrough of a traditional heritage house designed for Bhagamandala&ndash;Talakaveri Road, Kodagu (Coorg), Karnataka.</p>
  <div class="hero-actions">
    <a href="viewer.html" class="btn-primary">&#9654; Explore in 3D</a>
    <a href="#gallery" class="btn-secondary">&#9881; View Floor Plans</a>
  </div>
  <div class="hero-stats">
    <div class="hero-stat"><div class="val">2,909</div><div class="lbl">Sqft Built-up</div></div>
    <div class="hero-stat"><div class="val">G+1</div><div class="lbl">Two Floors</div></div>
    <div class="hero-stat"><div class="val">18</div><div class="lbl">Rooms</div></div>
    <div class="hero-stat"><div class="val">42&times;38</div><div class="lbl">Footprint (ft)</div></div>
  </div>
</header>

<section id="about" class="fade-up">
  <div class="about-grid">
    <div>
      <div class="section-label">About the Design</div>
      <h2 class="section-title">Heritage Meets Modern Living</h2>
      <p class="section-desc">Inspired by the Kodagu Gowda <em>Ainmane</em> tradition, this G+1 residence features exposed laterite stone walls, Mangalore tile roofing, and a 42-foot veranda with teak wood pillars &mdash; all on a 60&times;50 ft East-facing plot.</p>
      <div class="about-features">
        <div class="feat"><div class="feat-icon">&#9632;</div><h4>Exposed Laterite</h4><p>Bedroom walls in traditional <em>jambitt kallu</em> sealed with linseed oil. No plaster.</p></div>
        <div class="feat"><div class="feat-icon">&#9830;</div><h4>Mangalore Tiles</h4><p>Classic half-round clay tile roof with hip-and-gable profile.</p></div>
        <div class="feat"><div class="feat-icon">&#10070;</div><h4>Vastu Compliant</h4><p>East entrance, NE Pooja corner, SW Master Bedroom. Full alignment.</p></div>
        <div class="feat"><div class="feat-icon">&#9733;</div><h4>Ainmane Veranda</h4><p>42&times;8 ft <em>Jagali</em> with 5 teak pillars and Kota stone flooring.</p></div>
      </div>
    </div>
    <div class="about-img">
      <iframe src="viewer.html" loading="lazy" title="3D Preview"></iframe>
      <div class="overlay"></div>
    </div>
  </div>
</section>

<section id="gallery" class="gallery-section fade-up">
  <div style="text-align:center;margin-bottom:48px">
    <div class="section-label">Architectural Plans</div>
    <h2 class="section-title">Floor Plans & Elevations</h2>
    <p class="section-desc" style="margin-left:auto;margin-right:auto">Click any plan to view full size. All dimensions in feet.</p>
  </div>
  <div class="gallery-grid">
    <div class="gallery-card" onclick="openLB('img/GF_Plan_v4.png')"><img src="img/GF_Plan_v4.png" alt="Ground Floor Plan" loading="lazy"><div class="caption"><h4>Ground Floor Plan</h4><p>11 rooms &middot; Hall, Master BR, Kitchen, Veranda</p></div></div>
    <div class="gallery-card" onclick="openLB('img/FF_Plan_v4.png')"><img src="img/FF_Plan_v4.png" alt="First Floor Plan" loading="lazy"><div class="caption"><h4>First Floor Plan</h4><p>7 rooms &middot; FF Master, Family Hall, Study, Sitout</p></div></div>
    <div class="gallery-card" onclick="openLB('img/Front_Elevation_v4.png')"><img src="img/Front_Elevation_v4.png" alt="Front Elevation" loading="lazy"><div class="caption"><h4>Front Elevation (East)</h4><p>Road-facing &middot; Veranda pillars &middot; Mangalore tile roof</p></div></div>
    <div class="gallery-card" onclick="openLB('img/Back_Elevation_v4.png')"><img src="img/Back_Elevation_v4.png" alt="Back Elevation" loading="lazy"><div class="caption"><h4>Back Elevation (West)</h4><p>Coffee estate view &middot; FF Sitout &middot; Laterite walls</p></div></div>
    <div class="gallery-card" onclick="openLB('img/Site_Layout_v4.png')"><img src="img/Site_Layout_v4.png" alt="Site Layout" loading="lazy"><div class="caption"><h4>Site Layout</h4><p>60&times;50 ft plot &middot; Compound wall &middot; Vehicle parking</p></div></div>
    <div class="gallery-card" onclick="openLB('img/Roof_Solar_v4.png')"><img src="img/Roof_Solar_v4.png" alt="Roof & Solar Plan" loading="lazy"><div class="caption"><h4>Roof & Solar Plan</h4><p>Mangalore tiles &middot; Solar panel zones &middot; Rainwater</p></div></div>
  </div>
</section>

<section id="specs" class="fade-up">
  <div style="text-align:center;margin-bottom:48px">
    <div class="section-label">Specifications</div>
    <h2 class="section-title">Room-by-Room Details</h2>
  </div>
  <div class="specs-grid">
    <div class="spec-card">
      <h3>Ground Floor</h3>
      <div class="spec-row"><span class="k">Hall / Living</span><span class="v">16&times;16 = 256 sqft</span></div>
      <div class="spec-row"><span class="k">Master Bedroom</span><span class="v">16&times;16 = 256 sqft</span></div>
      <div class="spec-row"><span class="k">Bedroom 2 (Guest)</span><span class="v">14&times;14 = 196 sqft</span></div>
      <div class="spec-row"><span class="k">Kitchen</span><span class="v">16&times;14 = 224 sqft</span></div>
      <div class="spec-row"><span class="k">Store Room</span><span class="v">10&times;8 = 80 sqft</span></div>
      <div class="spec-row"><span class="k">Bathrooms (2)</span><span class="v">10&times;7 each</span></div>
      <div class="spec-row"><span class="k">Veranda / Jagali</span><span class="v">42&times;8 = 336 sqft</span></div>
    </div>
    <div class="spec-card">
      <h3>First Floor</h3>
      <div class="spec-row"><span class="k">FF Master Bedroom</span><span class="v">16&times;16 = 256 sqft</span></div>
      <div class="spec-row"><span class="k">Family Hall / TV</span><span class="v">16&times;14 = 224 sqft</span></div>
      <div class="spec-row"><span class="k">Work Room / Study</span><span class="v">10&times;14 = 140 sqft</span></div>
      <div class="spec-row"><span class="k">Bath 3 (FF Master)</span><span class="v">10&times;7 = 70 sqft</span></div>
      <div class="spec-row"><span class="k">Covered Sitout</span><span class="v">26&times;8 = 208 sqft</span></div>
      <div class="spec-row"><span class="k">Staircase</span><span class="v">10&times;5 = 50 sqft</span></div>
    </div>
    <div class="spec-card">
      <h3>Site & Structure</h3>
      <div class="spec-row"><span class="k">Plot Size</span><span class="v">60 &times; 50 ft</span></div>
      <div class="spec-row"><span class="k">Building</span><span class="v">42 &times; 38 ft</span></div>
      <div class="spec-row"><span class="k">Orientation</span><span class="v">East-facing</span></div>
      <div class="spec-row"><span class="k">Floors</span><span class="v">G + 1</span></div>
      <div class="spec-row"><span class="k">Bedrooms</span><span class="v">3</span></div>
      <div class="spec-row"><span class="k">Bathrooms</span><span class="v">3 + Guest WC</span></div>
      <div class="spec-row"><span class="k">Vastu</span><span class="v">&#10003; Compliant</span></div>
    </div>
  </div>
</section>

<section id="materials" class="fade-up">
  <div style="text-align:center;margin-bottom:48px">
    <div class="section-label">Materials Palette</div>
    <h2 class="section-title">Traditional & Natural Materials</h2>
  </div>
  <div class="materials-grid">
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#B06848,#8B4A30)"></div><h4>Laterite Stone</h4><div class="mat-use">Bedroom Walls</div><p>Local <em>jambitt kallu</em>. Exposed &amp; sealed with linseed oil. Kodagu heritage.</p></div>
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#B85C38,#8B3A1A)"></div><h4>Mangalore Tiles</h4><div class="mat-use">Roof</div><p>Half-round clay tiles from Mangalore/Udupi. Traditional hip-gable profile.</p></div>
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#C0AC88,#A08860)"></div><h4>Kota Stone</h4><div class="mat-use">Veranda Flooring</div><p>Natural limestone from Rajasthan. Hardwearing &amp; cool underfoot.</p></div>
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#C4A67A,#8B6914)"></div><h4>Teak Wood</h4><div class="mat-use">Pillars, Doors, Frames</div><p>5 veranda pillars, all doors &amp; window frames. Kerala/Karnataka sourced.</p></div>
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#E0EDED,#B0C4C4)"></div><h4>Ceramic Tiles</h4><div class="mat-use">Bathrooms</div><p>Anti-skid ceramic flooring. Walls tiled to 7 ft height. Rain showers.</p></div>
    <div class="mat-card"><div class="mat-swatch" style="background:linear-gradient(135deg,#BFBFB0,#888878)"></div><h4>Granite</h4><div class="mat-use">Steps &amp; Basins</div><p>Staircase steps and bathroom wash basins. Local grey granite.</p></div>
  </div>
</section>

<section class="heritage fade-up">
  <div class="heritage-content">
    <div class="section-label">Kodagu Heritage</div>
    <blockquote>&ldquo;In every laterite stone lives the warmth of generations. The Ainmane is not just a house &mdash; it is memory made shelter.&rdquo;</blockquote>
    <cite>&mdash; Kodagu Gowda Tradition</cite>
    <div class="heritage-tags">
      <span class="heritage-tag">&#9670; Ainmane Style</span>
      <span class="heritage-tag">&#9671; Laterite &middot; &#x0C9C;&#x0C82;&#x0CAC;&#x0CBF;&#x0C9F;&#x0CCD; &#x0C95;&#x0CB2;&#x0CCD;&#x0CB2;&#x0CC1;</span>
      <span class="heritage-tag">&#9830; Kodagu Gowda</span>
      <span class="heritage-tag">&#9733; Hare Bashe</span>
    </div>
  </div>
</section>

<section class="cta-section">
  <h2>Walk Through Your Future Home</h2>
  <p>Explore every room, material, and view in an interactive 3D experience.</p>
  <a href="viewer.html" class="btn-primary" style="font-size:16px;padding:16px 40px">&#9654; Launch 3D Walkthrough</a>
</section>

<footer>
  <div class="copy">Bhagamandala Heritage House &mdash; Kodagu, Karnataka &middot; Built by <a href="https://github.com/rakshith-ponnappa" target="_blank">Rakshith Ponnappa</a></div>
  <div class="links">
    <a href="viewer.html">3D Viewer</a>
    <a href="#gallery">Plans</a>
    <a href="#specs">Specs</a>
    <a href="https://github.com/rakshith-ponnappa/bhagamandala-house-3d" target="_blank">GitHub</a>
  </div>
</footer>

<div class="lightbox" id="lb" onclick="closeLB()">
  <div class="close">&times;</div>
  <img id="lbImg" src="" alt="">
</div>

<script>
// Lightbox
function openLB(src){document.getElementById('lbImg').src=src;document.getElementById('lb').classList.add('open')}
function closeLB(){document.getElementById('lb').classList.remove('open')}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeLB()});

// Nav scroll effect
const nav=document.getElementById('nav');
window.addEventListener('scroll',()=>{nav.classList.toggle('scrolled',window.scrollY>60)});

// Fade-up on scroll
const obs=new IntersectionObserver((entries)=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}})},{threshold:0.15});
document.querySelectorAll('.fade-up').forEach(el=>obs.observe(el));
</script>
</body>
</html>'''

with open(os.path.join(DOCS, "index.html"), "w") as f:
    f.write(LANDING)

# ── Copy viewer to docs/viewer.html ──────────────────────────────────
shutil.copy2(VIEWER_SRC, os.path.join(DOCS, "viewer.html"))

print("✓ docs/index.html  — Landing page")
print("✓ docs/viewer.html  — 3D Viewer")
print(f"✓ docs/img/         — {len(os.listdir(IMG_DIR))} plan images")
print("Done.")
