#!/usr/bin/env python3
"""
vmqtg-new-site — parallel build of Văn Miếu – Quốc Tử Giám website with a
modernised visual system. Reuses the content pipeline from ``site/build.py``
(docx→Article parsing, image resizing, bilingual/trilingual merging, caption
handling) but overrides:

  * output paths  (→ vmqtg-new-site/)
  * BASE_PATH     (→ /vmqtg-old-site/vmqtg-new-site on GitHub Pages)
  * CSS           (bright paper canvas + Playfair Display + Be Vietnam Pro)
  * page()        (sticky header + announcement bar + rich footer)
  * render_article / render_listing / render_section_index / render_program
  * build_home()  (editorial homepage: hero → quick-info → story → bento → …)

Run:
    python3 vmqtg-new-site/build.py
    BASE_PATH=/vmqtg-old-site/vmqtg-new-site python3 vmqtg-new-site/build.py
"""
import os
import sys
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
NEW_SITE = Path(__file__).resolve().parent

# Import the existing build module as a library, then rebind paths.
sys.path.insert(0, str(ROOT / "site"))
import build as vm  # type: ignore

vm.SITE = NEW_SITE
vm.ASSETS = NEW_SITE / "assets"
vm.IMG_DIR = NEW_SITE / "assets" / "images"
vm.BASE_PATH = os.environ.get(
    "BASE_PATH", "/vmqtg-old-site/vmqtg-new-site"
).rstrip("/")


# =========================================================================
# CSS
# =========================================================================
NEW_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

:root {
  --brick:       #8b2e2e;
  --brick-dark:  #5a1818;
  --brick-light: #a94444;
  --gold:        #c9a14a;
  --gold-soft:   #e4c988;
  --gold-pale:   #f6ead0;
  --paper:       #ffffff;
  --cream:       #faf6ee;
  --cream-soft:  #f5efe2;
  --ink:         #1c1917;
  --ink-soft:    #57524e;
  --ink-mute:    #8a837c;
  --line:        #ece5d3;
  --line-soft:   #f2ecdd;
  --shadow-sm:   0 1px 2px rgba(44,27,20,.06);
  --shadow-md:   0 4px 16px rgba(44,27,20,.08);
  --shadow-lg:   0 16px 40px rgba(44,27,20,.10);
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   16px;
  --container:   1200px;
  --nav-h:       72px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Be Vietnam Pro", "Noto Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16px; line-height: 1.6;
  color: var(--ink); background: var(--paper);
  -webkit-font-smoothing: antialiased;
}
img { max-width: 100%; display: block; }
a  { color: var(--brick); text-decoration: none; transition: color .2s; }
a:hover { color: var(--brick-dark); }
button { font: inherit; cursor: pointer; }
svg { display: block; }
:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; border-radius: 4px; }

.container { max-width: var(--container); margin: 0 auto; padding: 0 24px; }
.eyebrow {
  font-size: 12px; font-weight: 600; letter-spacing: .18em;
  text-transform: uppercase; color: var(--brick);
  display: inline-flex; align-items: center; gap: 10px;
}
.eyebrow::before { content: ""; width: 28px; height: 1px; background: var(--gold); }
.display { font-family: "Playfair Display", Georgia, serif; font-weight: 500; letter-spacing: -.01em; line-height: 1.1; }
.section-title {
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(28px, 3.6vw, 44px); font-weight: 500;
  color: var(--ink); margin: 12px 0 10px;
  letter-spacing: -.015em; line-height: 1.15;
}
.section-lede { font-size: 17px; color: var(--ink-soft); max-width: 620px; margin: 0 0 36px; line-height: 1.65; }
.section { padding: 88px 0; }
.section--cream { background: var(--cream); }
.section--paper { background: var(--paper); }
.section + .section { border-top: 1px solid var(--line-soft); }

/* ========== HEADER ========== */
.top-announce { background: var(--brick-dark); color: var(--cream-soft); font-size: 13px; }
.top-announce .container {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 24px; gap: 16px; flex-wrap: wrap;
}
.announce-items { display: flex; gap: 20px; flex-wrap: wrap; align-items: center; }
.announce-items span { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.announce-items svg { width: 14px; height: 14px; stroke: var(--gold-soft); }
.lang-pick a {
  color: var(--cream-soft); padding: 2px 8px; border-radius: 3px;
  font-weight: 500; font-size: 12px; letter-spacing: .05em;
}
.lang-pick a.is-active { background: var(--gold); color: var(--brick-dark); }
.lang-pick a:not(.is-active):hover { background: rgba(255,255,255,.08); color: #fff; }

.site-header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(255,255,255,.92);
  backdrop-filter: saturate(180%) blur(10px);
  -webkit-backdrop-filter: saturate(180%) blur(10px);
  border-bottom: 1px solid var(--line-soft);
}
.site-header .container {
  display: flex; align-items: center; justify-content: space-between;
  min-height: var(--nav-h);
}
.brand { display: flex; align-items: center; gap: 14px; text-decoration: none; }
.brand-mark {
  width: 44px; height: 44px; border-radius: 50%; background: var(--brick);
  color: var(--gold-soft); display: flex; align-items: center; justify-content: center;
  font-family: "Playfair Display", serif; font-weight: 700; font-size: 18px; font-style: italic;
  box-shadow: 0 0 0 2px var(--gold-soft) inset;
}
.brand-text .name { font-family: "Playfair Display", serif; font-weight: 600; font-size: 18px; color: var(--ink); line-height: 1.1; }
.brand-text .sub { font-size: 11px; color: var(--ink-mute); letter-spacing: .06em; text-transform: uppercase; margin-top: 2px; }
.main-nav { display: flex; align-items: center; gap: 4px; }
.main-nav a { padding: 10px 14px; font-size: 14px; font-weight: 500; color: var(--ink); border-radius: var(--radius-sm); }
.main-nav a:hover, .main-nav a.active { background: var(--cream); color: var(--brick); }
.main-nav a.active { color: var(--brick); }
.nav-cta {
  margin-left: 10px; background: var(--brick) !important; color: #fff !important;
  padding: 10px 18px !important; font-weight: 600 !important; border-radius: 999px !important;
}
.nav-cta:hover { background: var(--brick-dark) !important; color: #fff !important; }
.menu-toggle { display: none; background: none; border: 0; padding: 8px; color: var(--ink); }

/* ========== HERO (home) ========== */
.hero { position: relative; min-height: 620px; overflow: hidden; color: #fff; }
.hero__media { position: absolute; inset: 0; z-index: 0; }
.hero__media::after {
  content: ""; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 30%, rgba(201,161,74,.12), transparent 60%);
}
.hero__content { position: relative; z-index: 1; padding: 120px 24px 88px; max-width: var(--container); margin: 0 auto; }
.hero__kicker {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 12px; font-weight: 600; letter-spacing: .2em;
  text-transform: uppercase; color: var(--gold-soft); margin-bottom: 18px;
}
.hero__kicker::before, .hero__kicker::after { content: ""; width: 32px; height: 1px; background: var(--gold-soft); }
.hero h1 {
  font-family: "Playfair Display", serif; font-weight: 500;
  font-size: clamp(40px, 6.4vw, 88px); line-height: 1.02; letter-spacing: -.02em;
  margin: 0 0 20px; max-width: 12ch;
}
.hero h1 em { font-style: italic; color: var(--gold-soft); font-weight: 400; }
.hero__lede { font-size: clamp(16px, 1.5vw, 19px); max-width: 560px; color: rgba(255,255,255,.92); line-height: 1.55; margin: 0 0 32px; }
.hero__ctas { display: flex; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 26px; font-size: 15px; font-weight: 600;
  border-radius: 999px; transition: all .2s ease;
  border: 1px solid transparent; line-height: 1; text-decoration: none;
}
.btn--primary { background: var(--brick); color: #fff; box-shadow: var(--shadow-md); }
.btn--primary:hover { background: var(--brick-dark); color: #fff; transform: translateY(-1px); box-shadow: var(--shadow-lg); }
.btn--ghost { background: transparent; color: #fff; border-color: rgba(255,255,255,.55); }
.btn--ghost:hover { background: rgba(255,255,255,.1); border-color: #fff; color: #fff; }
.btn--light { background: #fff; color: var(--brick); border-color: var(--line); }
.btn--light:hover { background: var(--cream); color: var(--brick-dark); }
.btn svg { width: 16px; height: 16px; }
.hero__scroll {
  position: absolute; left: 50%; bottom: 24px; transform: translateX(-50%);
  color: rgba(255,255,255,.7); font-size: 12px;
  letter-spacing: .15em; text-transform: uppercase;
  display: flex; flex-direction: column; align-items: center; gap: 8px; z-index: 1;
}
.hero__scroll .arrow { width: 1px; height: 28px; background: rgba(255,255,255,.7); animation: scrollCue 2s ease-in-out infinite; }
@keyframes scrollCue {
  0%, 100% { transform: scaleY(.4); opacity: .4; transform-origin: top; }
  50%      { transform: scaleY(1);  opacity: 1; }
}

/* ========== QUICK INFO BAR ========== */
.quickbar { margin-top: -56px; position: relative; z-index: 2; }
.quickbar__card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg); padding: 8px;
  display: grid; grid-template-columns: repeat(4, 1fr);
}
.quickbar__item { padding: 20px 22px; display: flex; gap: 14px; align-items: flex-start; border-right: 1px solid var(--line-soft); }
.quickbar__item:last-child { border-right: 0; }
.quickbar__icon {
  flex: 0 0 40px; width: 40px; height: 40px; border-radius: 50%;
  background: var(--gold-pale); display: flex; align-items: center; justify-content: center;
  color: var(--brick);
}
.quickbar__icon svg { width: 20px; height: 20px; }
.quickbar__label { font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--ink-mute); margin-bottom: 4px; }
.quickbar__value { font-weight: 600; color: var(--ink); font-size: 15px; line-height: 1.3; }
.quickbar__meta { font-size: 13px; color: var(--ink-soft); margin-top: 2px; }

/* ========== STORY ========== */
.story { display: grid; grid-template-columns: 1fr 1fr; gap: 72px; align-items: center; }
.story__media {
  position: relative; border-radius: var(--radius-lg); overflow: hidden;
  box-shadow: var(--shadow-lg); aspect-ratio: 4/5; background: var(--cream-soft);
}
.story__media img { width: 100%; height: 100%; object-fit: cover; }
.story__media::after {
  content: ""; position: absolute; inset: 0;
  border: 1px solid rgba(201,161,74,.45); border-radius: inherit; pointer-events: none;
}
.story__body p { font-size: 17px; color: var(--ink-soft); line-height: 1.75; margin: 0 0 18px; }
.story__body p strong { color: var(--ink); font-weight: 600; }
.story__pullquote {
  font-family: "Playfair Display", serif; font-style: italic;
  font-size: 22px; line-height: 1.5; color: var(--ink);
  padding-left: 20px; border-left: 3px solid var(--gold); margin: 28px 0;
}
.story__facts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 32px; padding-top: 28px; border-top: 1px solid var(--line); }
.fact__number { font-family: "Playfair Display", serif; font-size: 36px; font-weight: 600; color: var(--brick); line-height: 1; }
.fact__label { font-size: 13px; color: var(--ink-soft); margin-top: 6px; line-height: 1.4; }

/* ========== BENTO ========== */
.bento { display: grid; grid-template-columns: repeat(6, 1fr); grid-auto-rows: 180px; gap: 16px; }
.bento__tile {
  position: relative; overflow: hidden; border-radius: var(--radius-md);
  background: var(--cream-soft) center/cover no-repeat; color: #fff;
  display: flex; align-items: flex-end; padding: 22px;
  text-decoration: none; transition: transform .3s, box-shadow .3s; isolation: isolate;
}
.bento__tile::before {
  content: ""; position: absolute; inset: 0; z-index: -1;
  background: linear-gradient(180deg, transparent 40%, rgba(0,0,0,.75) 100%);
}
.bento__tile:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); color: #fff; }
.bento__tile:hover .bento__arrow { transform: translateX(6px); }
.bento__inner { position: relative; z-index: 1; }
.bento__kicker { font-size: 11px; font-weight: 600; letter-spacing: .15em; text-transform: uppercase; color: var(--gold-soft); }
.bento__title { font-family: "Playfair Display", serif; font-size: clamp(20px, 2vw, 26px); font-weight: 500; margin: 6px 0 4px; line-height: 1.15; }
.bento__desc { font-size: 13px; color: rgba(255,255,255,.85); line-height: 1.4; max-width: 32ch; }
.bento__arrow {
  position: absolute; top: 18px; right: 18px; z-index: 2;
  width: 36px; height: 36px; border-radius: 50%;
  background: rgba(255,255,255,.18); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center; color: #fff;
  transition: transform .25s;
}
.bento__arrow svg { width: 16px; height: 16px; }
.bento__tile--hero    { grid-column: span 4; grid-row: span 2; }
.bento__tile--tall    { grid-column: span 2; grid-row: span 2; }
.bento__tile--wide    { grid-column: span 3; }
.bento__tile--regular { grid-column: span 2; }

/* ========== VISIT ========== */
.visit { display: grid; grid-template-columns: 1.1fr .9fr; gap: 48px; align-items: start; }
.visit__map {
  background: var(--cream-soft); border-radius: var(--radius-lg); overflow: hidden;
  border: 1px solid var(--line); position: relative; aspect-ratio: 4/3;
}
.visit__map-illustration {
  position: relative; width: 100%; height: 100%;
  background:
    radial-gradient(ellipse at 25% 80%, rgba(201,161,74,.18), transparent 40%),
    radial-gradient(ellipse at 75% 30%, rgba(139,46,46,.08), transparent 50%),
    linear-gradient(180deg, #fdf8ea 0%, #f2ead3 100%);
}
.visit__map-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.visit__tips h3 { font-family: "Playfair Display", serif; font-size: 22px; font-weight: 600; margin: 24px 0 10px; color: var(--ink); }
.visit__tips h3:first-of-type { margin-top: 0; }
.visit__tips ul { list-style: none; padding: 0; margin: 0 0 16px; }
.visit__tips li { padding: 10px 0; border-bottom: 1px dashed var(--line); display: flex; gap: 14px; align-items: flex-start; font-size: 15px; color: var(--ink-soft); }
.visit__tips li strong { color: var(--ink); font-weight: 600; flex: 0 0 110px; }
.visit__tips li:last-child { border-bottom: 0; }
.visit__cta { display: inline-flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }

.precinct-list { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 32px 0 0; counter-reset: precinct; }
.precinct { text-align: center; padding: 16px 10px 18px; border-top: 2px solid var(--line); position: relative; counter-increment: precinct; }
.precinct::before {
  content: counter(precinct, decimal-leading-zero);
  font-family: "Playfair Display", serif; font-size: 13px; color: var(--brick);
  font-weight: 600; display: block; margin-bottom: 4px; letter-spacing: .08em;
}
.precinct h4 { font-size: 14px; font-weight: 600; color: var(--ink); margin: 0 0 4px; line-height: 1.3; }
.precinct p { font-size: 12px; color: var(--ink-soft); margin: 0; line-height: 1.4; }
.precinct:hover { border-top-color: var(--brick); background: var(--cream); }

/* ========== EXPLORE CARDS (3-col) ========== */
.explore-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.explore-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  overflow: hidden; display: flex; flex-direction: column; text-decoration: none; color: inherit;
  transition: border-color .25s, box-shadow .25s, transform .25s;
}
.explore-card:hover { border-color: var(--gold); box-shadow: var(--shadow-md); transform: translateY(-3px); color: inherit; }
.explore-card__media { aspect-ratio: 16/10; background: var(--cream-soft) center/cover no-repeat; position: relative; overflow: hidden; }
.explore-card__media::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 60%, rgba(0,0,0,.08) 100%); }
.explore-card__body { padding: 22px 24px 24px; display: flex; flex-direction: column; flex: 1; }
.explore-card__kicker { font-size: 11px; font-weight: 600; letter-spacing: .15em; text-transform: uppercase; color: var(--brick); }
.explore-card__title { font-family: "Playfair Display", serif; font-size: 22px; font-weight: 500; line-height: 1.2; margin: 8px 0 10px; color: var(--ink); letter-spacing: -.01em; }
.explore-card__desc { font-size: 14px; color: var(--ink-soft); margin: 0 0 16px; flex: 1; line-height: 1.55; }
.explore-card__more { font-size: 13px; font-weight: 600; color: var(--brick); display: inline-flex; align-items: center; gap: 6px; border-bottom: 1px solid transparent; padding-bottom: 1px; align-self: flex-start; }
.explore-card:hover .explore-card__more { border-bottom-color: var(--gold); }

/* ========== EDUCATION CARDS ========== */
.edu-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.edu-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 28px 24px 26px; display: flex; flex-direction: column;
  text-decoration: none; color: inherit; transition: transform .2s, border-color .2s;
  position: relative; overflow: hidden;
}
.edu-card::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--gold); transform: scaleX(0); transform-origin: left; transition: transform .3s; }
.edu-card:hover { transform: translateY(-2px); border-color: var(--gold); color: inherit; }
.edu-card:hover::before { transform: scaleX(1); }
.edu-card__age { font-family: "Playfair Display", serif; font-size: 44px; font-weight: 600; color: var(--brick); line-height: 1; margin-bottom: 4px; letter-spacing: -.02em; }
.edu-card__sub { font-size: 13px; color: var(--ink-mute); font-weight: 600; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 16px; }
.edu-card h4 { font-size: 16px; font-weight: 600; color: var(--ink); margin: 0 0 6px; line-height: 1.3; }
.edu-card p { font-size: 14px; color: var(--ink-soft); margin: 0 0 16px; line-height: 1.55; flex: 1; }
.edu-card__count { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; color: var(--brick); }

/* ========== ACTIVITIES ========== */
.activities { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: stretch; }
.activity { background: #fff; border: 1px solid var(--line); border-radius: var(--radius-lg); padding: 36px 36px 32px; display: flex; flex-direction: column; position: relative; overflow: hidden; }
.activity--featured { background: linear-gradient(135deg, var(--brick-dark) 0%, var(--brick) 100%); color: #fff; border-color: transparent; }
.activity--featured::before { content: ""; position: absolute; top: -40%; right: -20%; width: 70%; height: 180%; background: radial-gradient(circle, rgba(201,161,74,.25) 0%, transparent 60%); pointer-events: none; }
.activity__tag { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; letter-spacing: .15em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; background: var(--gold-pale); color: var(--brick); align-self: flex-start; }
.activity--featured .activity__tag { background: rgba(201,161,74,.25); color: var(--gold-soft); }
.activity h3 { font-family: "Playfair Display", serif; font-size: 26px; font-weight: 500; margin: 16px 0 10px; line-height: 1.2; }
.activity--featured h3 { color: #fff; }
.activity p { font-size: 15px; line-height: 1.6; margin: 0 0 18px; color: var(--ink-soft); flex: 1; }
.activity--featured p { color: rgba(255,255,255,.88); }
.activity a.btn { align-self: flex-start; }

/* ========== MULTILINGUAL ========== */
.multi { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; background: var(--cream); border-radius: var(--radius-lg); border: 1px solid var(--line); overflow: hidden; }
.multi__item { padding: 36px 32px; border-right: 1px solid var(--line-soft); text-align: center; }
.multi__item:last-child { border-right: 0; }
.multi__flag { font-family: "Playfair Display", serif; font-size: 12px; font-weight: 600; letter-spacing: .22em; color: var(--brick); text-transform: uppercase; display: inline-flex; align-items: center; gap: 10px; }
.multi__flag::before, .multi__flag::after { content: ""; width: 18px; height: 1px; background: var(--gold); }
.multi__greeting { font-family: "Playfair Display", serif; font-size: 28px; font-style: italic; font-weight: 400; color: var(--ink); margin: 12px 0 8px; }
.multi__desc { font-size: 14px; color: var(--ink-soft); margin: 0 0 14px; line-height: 1.55; }
.multi__link { font-size: 13px; font-weight: 600; color: var(--brick); display: inline-flex; align-items: center; gap: 6px; }

/* ========== PAGE TITLE (interior) ========== */
.page-hero {
  background: linear-gradient(180deg, var(--cream) 0%, #fff 100%);
  padding: 48px 0 44px;
  border-bottom: 1px solid var(--line-soft);
}
.page-hero .eyebrow { margin-bottom: 10px; }
.page-hero h1 {
  font-family: "Playfair Display", serif;
  font-size: clamp(32px, 4.5vw, 56px);
  font-weight: 500; line-height: 1.1; letter-spacing: -.02em;
  margin: 0 0 14px; color: var(--ink);
}
.page-hero .lede { font-size: 17px; max-width: 680px; color: var(--ink-soft); margin: 0; line-height: 1.65; }
.page-hero__actions { margin-top: 22px; display: flex; gap: 10px; flex-wrap: wrap; }

/* breadcrumbs */
.breadcrumbs {
  font-size: 13px; padding: 14px 0; color: var(--ink-mute);
  background: var(--paper); border-bottom: 1px solid var(--line-soft);
}
.breadcrumbs a { color: var(--ink-mute); }
.breadcrumbs a:hover { color: var(--brick); }
.breadcrumbs span.sep { margin: 0 8px; opacity: .6; }
.breadcrumbs span:not(.sep) { color: var(--ink); }

/* ========== LISTING (interior card grid) ========== */
main { padding: 0; }
.page-body { padding: 56px 0 88px; }
.section-hero {
  padding: 40px 0 32px;
}
.grid {
  display: grid; gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
.card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  overflow: hidden; display: flex; flex-direction: column; text-decoration: none; color: inherit;
  transition: transform .2s, border-color .2s, box-shadow .2s;
}
.card:hover { transform: translateY(-3px); border-color: var(--gold); box-shadow: var(--shadow-md); color: inherit; }
.card .thumb {
  width: 100%; aspect-ratio: 16/10; background: var(--cream-soft) center/cover no-repeat;
  border-bottom: 1px solid var(--line-soft);
}
.card .thumb--empty {
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--brick) 0%, var(--brick-dark) 100%);
  color: var(--gold-soft); font-family: "Playfair Display", serif;
  font-size: 42px; font-weight: 600; font-style: italic;
}
.card .body { padding: 22px 24px 24px; flex: 1; display: flex; flex-direction: column; }
.card h3 { margin: 0 0 8px; font-family: "Playfair Display", serif; font-size: 20px; font-weight: 500; color: var(--ink); line-height: 1.25; letter-spacing: -.01em; }
.card p { margin: 0 0 16px; color: var(--ink-soft); font-size: 14px; flex: 1; line-height: 1.55; }
.card .more {
  font-size: 13px; font-weight: 600; color: var(--brick);
  display: inline-flex; align-items: center; gap: 6px;
  border-bottom: 1px solid transparent; padding-bottom: 1px; align-self: flex-start;
}
.card:hover .more { border-bottom-color: var(--gold); }

/* ========== HUB (section index) ========== */
.hub-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
.hub-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 28px 26px 26px; display: flex; flex-direction: column;
  text-decoration: none; color: inherit;
  transition: transform .2s, border-color .2s, box-shadow .2s;
  position: relative; overflow: hidden;
}
.hub-card::before {
  content: ""; position: absolute; top: 0; left: 0; bottom: 0; width: 3px;
  background: var(--gold); transform: scaleY(0); transform-origin: top; transition: transform .3s;
}
.hub-card:hover { transform: translateX(4px); border-color: var(--gold); box-shadow: var(--shadow-md); color: inherit; }
.hub-card:hover::before { transform: scaleY(1); }
.hub-card__count {
  font-family: "Playfair Display", serif; font-size: 13px; color: var(--brick);
  font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
}
.hub-card h3 {
  font-family: "Playfair Display", serif;
  font-size: 22px; font-weight: 500; color: var(--ink);
  margin: 8px 0 10px; line-height: 1.25;
}
.hub-card p { font-size: 14px; color: var(--ink-soft); margin: 0 0 18px; line-height: 1.55; flex: 1; }
.hub-card__more { font-size: 13px; font-weight: 600; color: var(--brick); align-self: flex-start; display: inline-flex; align-items: center; gap: 6px; }

/* ========== ARTICLE ========== */
article.article-body {
  max-width: 780px; margin: 0 auto;
  background: #fff; padding: 0;
  color: var(--ink);
}
article.article-body .article-meta {
  font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
  color: var(--brick); font-weight: 600; margin-bottom: 10px;
  display: inline-flex; align-items: center; gap: 10px;
}
article.article-body .article-meta::before { content: ""; width: 28px; height: 1px; background: var(--gold); }
article.article-body h1 {
  font-family: "Playfair Display", serif; font-weight: 500;
  font-size: clamp(30px, 4vw, 44px); line-height: 1.15; letter-spacing: -.015em;
  color: var(--ink); margin: 0 0 28px; padding-bottom: 20px;
  border-bottom: 1px solid var(--line);
}
article.article-body p { margin: 0 0 18px; font-size: 17px; line-height: 1.75; color: var(--ink-soft); }
article.article-body p:first-of-type::first-letter {
  font-family: "Playfair Display", serif; font-size: 3.2em;
  float: left; line-height: .9; padding: 4px 10px 0 0; color: var(--brick); font-weight: 600;
}
article.article-body h2 { font-family: "Playfair Display", serif; font-size: 26px; font-weight: 500; color: var(--ink); margin: 36px 0 14px; }
article.article-body h3 {
  font-family: "Playfair Display", serif; font-weight: 500;
  font-size: 22px; color: var(--ink); margin: 32px 0 12px; letter-spacing: -.01em;
}
article.article-body img {
  max-width: 100%; height: auto; display: block; margin: 28px auto;
  border-radius: var(--radius-md); box-shadow: var(--shadow-sm);
}
article.article-body .gallery {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px; margin: 28px 0;
}
article.article-body .gallery a {
  display: block; overflow: hidden; border-radius: var(--radius-sm);
  background: var(--cream-soft); cursor: zoom-in; position: relative;
  border: 1px solid var(--line-soft);
}
article.article-body .gallery a::after {
  content: "⤢"; position: absolute; right: 6px; bottom: 4px;
  color: #fff; background: rgba(0,0,0,.55); padding: 2px 7px;
  border-radius: 2px; font-size: 12px; opacity: 0; transition: opacity .15s;
}
article.article-body .gallery a:hover::after { opacity: 1; }
article.article-body .gallery img {
  margin: 0; padding: 0; border: 0; border-radius: 0;
  width: 100%; height: 180px; object-fit: cover;
  display: block; transition: transform .3s; box-shadow: none;
}
article.article-body .gallery a:hover img { transform: scale(1.04); }
article.article-body .gallery .caption {
  display: block; font-size: 12px; color: var(--ink-mute);
  padding: 6px 8px; line-height: 1.35; background: #fff;
  border-top: 1px solid var(--line-soft);
}

/* language toggles (details/summary) */
article.article-body details.lang-block {
  margin: 28px 0 0; background: var(--cream); border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 18px 24px; transition: background .2s;
}
article.article-body details.lang-block[open] { background: var(--paper); box-shadow: var(--shadow-sm); }
article.article-body details.lang-block > summary {
  cursor: pointer; font-weight: 600; color: var(--brick); list-style: none;
  display: flex; align-items: center; gap: 10px;
  font-size: 14px; letter-spacing: .04em;
}
article.article-body details.lang-block > summary::-webkit-details-marker { display: none; }
article.article-body details.lang-block > summary::before {
  content: "+"; display: inline-flex; width: 22px; height: 22px;
  align-items: center; justify-content: center; background: var(--gold-pale);
  color: var(--brick); border-radius: 50%; font-weight: 700; transition: transform .2s;
}
article.article-body details.lang-block[open] > summary::before { content: "−"; }
article.article-body details.lang-block h2 { font-size: 22px; margin: 16px 0 10px; color: var(--ink); }

/* lightbox */
.lightbox { position: fixed; inset: 0; background: rgba(0,0,0,.92); display: none; align-items: center; justify-content: center; z-index: 1000; cursor: zoom-out; padding: 20px; }
.lightbox.open { display: flex; }
.lightbox img { max-width: 100%; max-height: 100%; box-shadow: 0 0 60px rgba(255,255,255,.1); }
.lightbox .close { position: absolute; top: 14px; right: 18px; color: #fff; font-size: 28px; cursor: pointer; line-height: 1; user-select: none; background: rgba(255,255,255,.1); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.lightbox .nav { position: absolute; top: 50%; transform: translateY(-50%); color: #fff; font-size: 40px; cursor: pointer; user-select: none; padding: 14px 20px; background: rgba(255,255,255,.08); }
.lightbox .nav:hover { background: rgba(255,255,255,.2); }
.lightbox .prev { left: 12px; }
.lightbox .next { right: 12px; }
.lightbox .counter { position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%); color: #fff; font-size: 13px; background: rgba(0,0,0,.5); padding: 4px 12px; border-radius: 12px; }

/* ========== THAM QUAN ========== */
.visit-hero {
  position: relative; min-height: 440px; overflow: hidden; color: #fff;
  display: flex; align-items: flex-end;
}
.visit-hero__media { position: absolute; inset: 0; z-index: 0; }
.visit-hero__content { position: relative; z-index: 1; padding: 88px 0 64px; max-width: var(--container); width: 100%; margin: 0 auto; }
.visit-hero__kicker { display: inline-flex; align-items: center; gap: 10px; font-size: 12px; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--gold-soft); margin-bottom: 18px; }
.visit-hero__kicker::before { content: ""; width: 32px; height: 1px; background: var(--gold-soft); }
.visit-hero h1 { font-family: "Playfair Display", serif; font-weight: 500; font-size: clamp(36px, 5.5vw, 68px); line-height: 1.05; letter-spacing: -.02em; margin: 0 0 18px; max-width: 14ch; }
.visit-hero h1 em { font-style: italic; color: var(--gold-soft); }
.visit-hero__lede { font-size: clamp(16px, 1.4vw, 18px); max-width: 560px; color: rgba(255,255,255,.9); line-height: 1.55; margin: 0; }

.visit-info { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: stretch; }
.info-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 28px 30px 26px; display: flex; flex-direction: column;
}
.info-card__eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .15em; text-transform: uppercase; color: var(--brick); margin-bottom: 6px; }
.info-card h3 { font-family: "Playfair Display", serif; font-size: 24px; font-weight: 500; margin: 0 0 18px; color: var(--ink); letter-spacing: -.01em; }
.hours-table, .price-table { width: 100%; border-collapse: collapse; }
.hours-table td, .price-table td { padding: 14px 0; border-bottom: 1px dashed var(--line); font-size: 15px; vertical-align: top; }
.hours-table tr:last-child td, .price-table tr:last-child td { border-bottom: 0; }
.hours-table td:first-child, .price-table td:first-child { color: var(--ink); font-weight: 500; }
.hours-table td:last-child, .price-table td:last-child { text-align: right; font-weight: 600; color: var(--brick); font-variant-numeric: tabular-nums; }
.hours-table tr.is-highlight td { color: var(--brick-dark); }
.hours-table tr.is-highlight td:first-child::before { content: "•"; color: var(--gold); margin-right: 8px; font-size: 18px; }
.price-table .price-row__title { font-weight: 500; color: var(--ink); }
.price-table .price-row__sub { font-size: 12px; color: var(--ink-mute); margin-top: 2px; font-weight: 400; }
.price-table tr.is-featured td { background: var(--gold-pale); border-radius: var(--radius-sm); }
.price-table tr.is-featured td:first-child { padding-left: 12px; border-radius: var(--radius-sm) 0 0 var(--radius-sm); }
.price-table tr.is-featured td:last-child { padding-right: 12px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; color: var(--brick-dark); }
.price-table tr.is-free td:last-child { color: #059669; }
.info-card__cta {
  margin-top: 22px; display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px 22px; background: var(--brick); color: #fff; font-weight: 600; font-size: 15px;
  border-radius: 999px; text-decoration: none; transition: all .2s; width: 100%; box-sizing: border-box;
}
.info-card__cta:hover { background: var(--brick-dark); color: #fff; transform: translateY(-1px); box-shadow: var(--shadow-md); }
.info-card__cta svg { width: 16px; height: 16px; }

/* Map + transport */
.directions-map {
  border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--line);
  box-shadow: var(--shadow-sm); margin-bottom: 24px; position: relative; background: var(--cream);
}
.directions-map iframe { display: block; width: 100%; height: 420px; border: 0; }
.directions-map__cta {
  position: absolute; top: 16px; left: 16px; z-index: 2;
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 16px; background: #fff; color: var(--ink); font-weight: 600; font-size: 14px;
  border-radius: 999px; text-decoration: none; border: 1px solid var(--line);
  box-shadow: var(--shadow-md); transition: all .2s;
}
.directions-map__cta:hover { background: var(--brick); color: #fff; border-color: var(--brick); }
.directions-map__cta svg { width: 14px; height: 14px; }

.transport-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.transport-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 22px 22px 20px; display: flex; flex-direction: column; gap: 10px;
  transition: border-color .2s, transform .2s;
}
.transport-card:hover { border-color: var(--gold); transform: translateY(-2px); }
.transport-card__icon {
  width: 44px; height: 44px; border-radius: 50%; background: var(--gold-pale);
  color: var(--brick); display: flex; align-items: center; justify-content: center;
}
.transport-card__icon svg { width: 22px; height: 22px; }
.transport-card h4 { font-size: 15px; font-weight: 600; color: var(--ink); margin: 4px 0 2px; }
.transport-card p { font-size: 13px; color: var(--ink-soft); margin: 0; line-height: 1.5; }

/* Amenities */
.amenities-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.amenity {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  padding: 20px 16px 18px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 8px;
  transition: border-color .2s, background .2s;
}
.amenity:hover { border-color: var(--gold); background: var(--cream); }
.amenity__icon {
  width: 40px; height: 40px; border-radius: 50%; background: var(--gold-pale);
  color: var(--brick); display: flex; align-items: center; justify-content: center;
}
.amenity__icon svg { width: 20px; height: 20px; }
.amenity h4 { font-size: 13px; font-weight: 600; color: var(--ink); margin: 2px 0 0; line-height: 1.3; }
.amenity p { font-size: 11px; color: var(--ink-mute); margin: 2px 0 0; }

.a11y-banner {
  margin-top: 16px;
  background: linear-gradient(90deg, var(--gold-pale) 0%, #fff 100%);
  border: 1px solid var(--gold-soft); border-radius: var(--radius-md);
  padding: 20px 24px; display: flex; align-items: center; gap: 18px;
}
.a11y-banner__icon {
  flex: 0 0 48px; width: 48px; height: 48px; border-radius: 50%;
  background: var(--brick); color: var(--gold-soft);
  display: flex; align-items: center; justify-content: center;
}
.a11y-banner__icon svg { width: 24px; height: 24px; }
.a11y-banner h4 { margin: 0 0 4px; font-size: 15px; font-weight: 600; color: var(--ink); }
.a11y-banner p { margin: 0; font-size: 14px; color: var(--ink-soft); line-height: 1.5; }

/* Tours */
.tour-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.tour-card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  overflow: hidden; display: flex; flex-direction: column;
  transition: border-color .25s, box-shadow .25s, transform .25s;
}
.tour-card:hover { border-color: var(--gold); box-shadow: var(--shadow-md); transform: translateY(-3px); }
.tour-card__media {
  aspect-ratio: 16/9; background: var(--cream-soft) center/cover no-repeat;
  position: relative;
}
.tour-card__media::after {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, transparent 40%, rgba(0,0,0,.55) 100%);
}
.tour-card__tag {
  position: absolute; top: 16px; left: 16px; z-index: 2;
  padding: 6px 12px; background: rgba(255,255,255,.95); color: var(--brick);
  font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
  border-radius: 999px; backdrop-filter: blur(6px);
}
.tour-card__body { padding: 24px 26px 26px; display: flex; flex-direction: column; flex: 1; }
.tour-card__meta {
  display: flex; align-items: center; gap: 14px; font-size: 13px; color: var(--ink-mute);
  margin-bottom: 10px;
}
.tour-card__meta .duration { display: inline-flex; align-items: center; gap: 4px; }
.tour-card__meta .price { color: var(--brick); font-weight: 700; font-size: 15px; font-variant-numeric: tabular-nums; }
.tour-card h3 {
  font-family: "Playfair Display", serif; font-size: 24px; font-weight: 500;
  color: var(--ink); margin: 0 0 10px; line-height: 1.2; letter-spacing: -.01em;
}
.tour-card p { font-size: 14px; color: var(--ink-soft); margin: 0 0 16px; line-height: 1.55; }
.tour-card ul { margin: 0 0 20px; padding: 0; list-style: none; }
.tour-card li { padding: 6px 0 6px 22px; position: relative; font-size: 14px; color: var(--ink-soft); line-height: 1.5; }
.tour-card li::before {
  content: ""; position: absolute; left: 0; top: 14px;
  width: 14px; height: 2px; background: var(--gold);
}
.tour-card__cta { align-self: flex-start; margin-top: auto; }

/* Booking form */
.booking-section {
  background: var(--cream); border: 1px solid var(--line); border-radius: var(--radius-lg);
  padding: 40px 44px 36px;
}
.booking-form {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px 20px;
  margin-top: 24px;
}
.booking-form .field { display: flex; flex-direction: column; gap: 6px; }
.booking-form .field--full { grid-column: span 2; }
.booking-form label {
  font-size: 13px; font-weight: 600; color: var(--ink);
  letter-spacing: .02em;
}
.booking-form input,
.booking-form select,
.booking-form textarea {
  padding: 12px 14px; font: inherit; font-size: 14px;
  border: 1px solid var(--line); background: #fff; color: var(--ink);
  border-radius: var(--radius-sm);
  transition: border-color .2s, box-shadow .2s;
}
.booking-form input:focus,
.booking-form select:focus,
.booking-form textarea:focus {
  outline: none; border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(201, 161, 74, .2);
}
.booking-form textarea { resize: vertical; min-height: 96px; font-family: inherit; }
.booking-form__submit {
  grid-column: span 2; margin-top: 8px;
  padding: 16px 28px; background: var(--brick); color: #fff;
  font-size: 15px; font-weight: 600; border: 0; border-radius: 999px;
  cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  transition: all .2s;
}
.booking-form__submit:hover { background: var(--brick-dark); transform: translateY(-1px); box-shadow: var(--shadow-md); }
.booking-form__submit svg { width: 16px; height: 16px; }

/* Services list (replaces booking form — real contact info per service) */
.services-list { display: flex; flex-direction: column; gap: 14px; }
.service-row {
  display: grid; grid-template-columns: auto 1fr auto;
  gap: 20px; align-items: center;
  padding: 20px 24px; background: #fff;
  border: 1px solid var(--line); border-radius: var(--radius-md);
  transition: border-color .2s;
}
.service-row:hover { border-color: var(--gold); }
.service-row__icon {
  flex: 0 0 44px; width: 44px; height: 44px; border-radius: 50%;
  background: var(--gold-pale); color: var(--brick);
  display: flex; align-items: center; justify-content: center;
}
.service-row__icon svg { width: 20px; height: 20px; }
.service-row__body h3 {
  font-family: "Playfair Display", serif;
  font-size: 18px; font-weight: 500; color: var(--ink);
  margin: 0 0 4px; letter-spacing: -.01em; line-height: 1.3;
}
.service-row__body p { font-size: 14px; color: var(--ink-soft); margin: 0; line-height: 1.55; }
.service-row__cta {
  display: flex; flex-direction: column; align-items: flex-end;
  padding-left: 20px; border-left: 1px solid var(--line);
  text-decoration: none; transition: color .2s;
}
.service-row__cta--info { cursor: default; }
.service-row__cta:hover:not(.service-row__cta--info) .service-row__tel { color: var(--brick-dark); }
.service-row__label {
  font-size: 11px; font-weight: 600; letter-spacing: .1em;
  text-transform: uppercase; color: var(--ink-mute); margin-bottom: 2px;
  white-space: nowrap;
}
.service-row__tel {
  font-size: 15px; font-weight: 700; color: var(--brick);
  font-variant-numeric: tabular-nums; white-space: nowrap;
}
.service-row__cta--info .service-row__tel { color: var(--ink); }

/* Rules highlight callout */
.rules-highlight {
  margin-top: 72px;
  display: grid; grid-template-columns: auto 1fr auto;
  gap: 28px; align-items: center;
  padding: 28px 32px;
  background: linear-gradient(90deg, var(--gold-pale) 0%, #fff 65%);
  border: 1px solid var(--gold-soft);
  border-radius: var(--radius-lg);
  text-decoration: none; color: inherit;
  transition: transform .2s, box-shadow .2s, border-color .2s;
}
.rules-highlight:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md); color: inherit;
  border-color: var(--gold);
}
.rules-highlight__icon {
  flex: 0 0 56px; width: 56px; height: 56px; border-radius: 50%;
  background: var(--brick); color: var(--gold-soft);
  display: flex; align-items: center; justify-content: center;
}
.rules-highlight__icon svg { width: 24px; height: 24px; }
.rules-highlight__eyebrow {
  font-size: 11px; font-weight: 600; letter-spacing: .15em;
  text-transform: uppercase; color: var(--brick);
}
.rules-highlight__body h3 {
  font-family: "Playfair Display", serif;
  font-size: 22px; font-weight: 500; color: var(--ink);
  margin: 4px 0 6px; letter-spacing: -.01em;
}
.rules-highlight__body p { font-size: 14px; color: var(--ink-soft); margin: 0; line-height: 1.55; }
.rules-highlight__cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px; background: var(--brick); color: #fff;
  font-size: 14px; font-weight: 600; border-radius: 999px;
  white-space: nowrap; transition: background .2s;
}
.rules-highlight:hover .rules-highlight__cta { background: var(--brick-dark); }
.rules-highlight__cta svg { width: 14px; height: 14px; }

/* Related docs (compact) */
.docs-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.docs-list__item {
  display: flex; align-items: center; gap: 14px;
  padding: 18px 20px; background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md);
  text-decoration: none; color: var(--ink);
  transition: border-color .2s, transform .2s;
}
.docs-list__item:hover { border-color: var(--gold); transform: translateX(3px); color: var(--ink); }
.docs-list__icon {
  flex: 0 0 36px; width: 36px; height: 36px; border-radius: var(--radius-sm);
  background: var(--gold-pale); color: var(--brick);
  display: flex; align-items: center; justify-content: center;
}
.docs-list__icon svg { width: 18px; height: 18px; }
.docs-list__title { font-size: 14px; font-weight: 600; line-height: 1.3; flex: 1; }

/* ========== NỘI QUY (creative) ========== */
.rules-hero {
  background: radial-gradient(ellipse at top right, var(--gold-pale) 0%, var(--cream) 45%, #fff 100%);
  padding: 72px 0 56px;
  text-align: center;
  border-bottom: 1px solid var(--line-soft);
}
.rules-hero .eyebrow { justify-content: center; margin-bottom: 14px; }
.rules-hero .eyebrow::before,
.rules-hero .eyebrow::after { content: ""; width: 28px; height: 1px; background: var(--gold); }
.rules-hero .eyebrow { display: inline-flex; gap: 12px; }
.rules-hero h1 {
  font-family: "Playfair Display", serif; font-weight: 500;
  font-size: clamp(32px, 4.4vw, 52px); line-height: 1.12;
  letter-spacing: -.015em; margin: 0 auto 18px; color: var(--ink); max-width: 18ch;
}
.rules-hero h1 em { font-style: italic; color: var(--brick); font-weight: 500; }
.rules-hero__lede { max-width: 640px; margin: 0 auto; font-size: 17px; color: var(--ink-soft); line-height: 1.65; }
.rules-hero__lede strong { color: var(--brick); font-weight: 600; }

/* Editorial numbered list (not cards — these are readable content, not links) */
.rules-list {
  max-width: 860px; margin: 8px auto 0;
  display: flex; flex-direction: column;
}
.rule-item {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 32px;
  align-items: flex-start;
  padding: 32px 0;
  border-bottom: 1px solid var(--line-soft);
}
.rule-item:last-child { border-bottom: 0; }
.rule-item__number {
  font-family: "Playfair Display", serif;
  font-size: 64px; font-weight: 500; font-style: italic;
  color: var(--gold); line-height: 1;
  text-align: right;
  font-variant-numeric: lining-nums;
  user-select: none;
  padding-top: 4px;
}
.rule-item__header {
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 12px;
}
.rule-item__icon {
  flex: 0 0 auto; color: var(--brick);
  display: inline-flex;
}
.rule-item__icon svg { width: 22px; height: 22px; }
.rule-item h3 {
  font-family: "Playfair Display", serif;
  font-size: 22px; font-weight: 500; color: var(--ink);
  margin: 0; letter-spacing: -.01em; line-height: 1.25;
}
.rule-item p {
  font-size: 16px; color: var(--ink-soft); line-height: 1.75; margin: 0;
  max-width: 65ch;
}

/* Closing scholar-note */
.rules-closing {
  margin: 56px auto 0; max-width: 640px; text-align: center;
  padding: 32px 24px;
}
.rules-closing__mark {
  display: inline-block; font-family: "Playfair Display", serif;
  font-size: 32px; color: var(--gold); line-height: 1; margin-bottom: 12px;
}
.rules-closing p {
  font-family: "Playfair Display", serif; font-style: italic;
  font-size: 22px; color: var(--ink); line-height: 1.5; margin: 0;
}

/* Emergency / hotline banner */
.emergency-card {
  margin-top: 48px;
  background: linear-gradient(135deg, var(--brick-dark) 0%, var(--brick) 100%);
  color: #fff; border-radius: var(--radius-lg);
  padding: 32px 36px; display: grid;
  grid-template-columns: auto 1fr auto; gap: 28px; align-items: center;
  position: relative; overflow: hidden;
}
.emergency-card::before {
  content: ""; position: absolute; top: -40%; right: -10%; width: 50%; height: 180%;
  background: radial-gradient(circle, rgba(201,161,74,.28) 0%, transparent 60%);
  pointer-events: none;
}
.emergency-card__icon {
  flex: 0 0 64px; width: 64px; height: 64px; border-radius: 50%;
  background: rgba(201,161,74,.22); color: var(--gold-soft);
  display: flex; align-items: center; justify-content: center;
  position: relative; z-index: 1;
}
.emergency-card__icon svg { width: 28px; height: 28px; }
.emergency-card__body { position: relative; z-index: 1; }
.emergency-card__eyebrow {
  font-size: 11px; font-weight: 600; letter-spacing: .18em; text-transform: uppercase;
  color: var(--gold-soft); display: block; margin-bottom: 4px;
}
.emergency-card__body h3 {
  font-family: "Playfair Display", serif; font-size: 22px; font-weight: 500;
  margin: 0 0 6px; color: #fff;
}
.emergency-card__body p { margin: 0; font-size: 14px; color: rgba(255,255,255,.85); line-height: 1.5; }
.emergency-card__numbers {
  display: flex; flex-direction: column; gap: 8px; position: relative; z-index: 1;
}
.emergency-card__tel {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px;
  background: rgba(255,255,255,.12); color: #fff;
  border: 1px solid rgba(255,255,255,.25);
  border-radius: 999px; font-weight: 600; font-size: 15px;
  font-variant-numeric: tabular-nums;
  text-decoration: none; transition: all .2s;
}
.emergency-card__tel:hover { background: #fff; color: var(--brick-dark); border-color: #fff; }

/* Pill-style language switcher inside rules-hero */
.rules-hero__tabs {
  margin: 28px auto 0;
  display: inline-flex; gap: 4px;
  padding: 4px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 999px;
  box-shadow: var(--shadow-sm);
}
.lang-tab {
  padding: 8px 20px; background: transparent; border: 0;
  font: inherit; font-size: 13px; font-weight: 600; color: var(--ink-mute);
  cursor: pointer; border-radius: 999px;
  transition: all .2s;
  letter-spacing: .02em;
}
.lang-tab:hover { color: var(--ink); background: var(--gold-pale); }
.lang-tab.is-active { color: #fff; background: var(--brick); }
.lang-tab.is-active:hover { background: var(--brick-dark); }
.lang-panel[hidden] { display: none; }

/* ========== FOOTER ========== */
.site-footer { background: var(--brick-dark); color: var(--cream-soft); padding: 72px 0 24px; border-top: 4px solid var(--gold); margin-top: 0; }
.site-footer a { color: var(--cream-soft); }
.site-footer a:hover { color: var(--gold-soft); }
.footer-grid { display: grid; grid-template-columns: 1.6fr 1fr 1fr 1fr; gap: 48px; padding-bottom: 48px; border-bottom: 1px solid rgba(255,255,255,.12); }
.footer-brand .brand { margin-bottom: 20px; }
.footer-brand .brand-text .name { color: #fff; }
.footer-brand .brand-text .sub { color: var(--gold-soft); }
.footer-brand p { font-size: 14px; line-height: 1.6; opacity: .85; margin: 0 0 16px; max-width: 360px; }
.footer-contact { display: flex; flex-direction: column; gap: 8px; font-size: 14px; }
.footer-contact span { display: inline-flex; align-items: center; gap: 8px; }
.footer-contact svg { width: 14px; height: 14px; stroke: var(--gold-soft); }
.footer-col h4 { font-family: "Playfair Display", serif; font-size: 15px; font-weight: 600; color: #fff; margin: 0 0 14px; letter-spacing: .04em; }
.footer-col ul { list-style: none; margin: 0; padding: 0; }
.footer-col li { padding: 5px 0; font-size: 14px; }
.footer-bottom { padding: 20px 0 0; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: rgba(255,255,255,.6); flex-wrap: wrap; gap: 12px; }
.footer-bottom .legal { display: flex; gap: 18px; }

/* ========== SITEMAP ========== */
.sm-toolbar { display: flex; gap: 10px; flex-wrap: wrap; margin: 18px 0 26px; padding: 14px 16px; background: var(--cream); border: 1px solid var(--line); border-radius: var(--radius-md); }
.sm-search { flex: 1 1 260px; min-width: 180px; padding: 10px 14px; font: inherit; border: 1px solid var(--line); background: #fff; color: var(--ink); border-radius: var(--radius-sm); }
.sm-search:focus { outline: 2px solid var(--gold); outline-offset: -1px; border-color: var(--gold); }
.sm-btn { padding: 8px 16px; border: 1px solid var(--brick); background: #fff; color: var(--brick); font: inherit; font-size: 14px; font-weight: 600; cursor: pointer; letter-spacing: .02em; border-radius: var(--radius-sm); }
.sm-btn:hover { background: var(--brick); color: #fff; }
.sm-stats { color: var(--ink-mute); font-size: 13px; font-style: italic; margin: -10px 0 16px; }
.sm-tree, .sm-tree ul { list-style: none; padding: 0; margin: 0; }
.sm-tree ul.sm-children { padding-left: 22px; margin-left: 10px; border-left: 1px dashed var(--line); }
.sm-node { padding: 2px 0; }
.sm-row { display: flex; align-items: center; gap: 2px; }
.sm-toggle { width: 22px; height: 22px; border: none; background: transparent; cursor: pointer; color: var(--brick); font-size: 11px; line-height: 1; padding: 0; display: inline-flex; align-items: center; justify-content: center; transition: transform .15s; flex: 0 0 auto; }
.sm-node.sm-open > .sm-row > .sm-toggle { transform: rotate(90deg); }
.sm-dot { display: inline-flex; width: 22px; justify-content: center; color: var(--ink-mute); flex: 0 0 auto; font-size: 12px; }
.sm-link { color: var(--ink); padding: 3px 8px; border-radius: 2px; flex: 1 1 auto; min-width: 0; }
.sm-link[href]:hover { background: var(--cream); color: var(--brick); }
.sm-count { display: inline-block; margin-left: 8px; padding: 1px 9px; background: #fff; color: var(--ink-mute); border: 1px solid var(--line); border-radius: 12px; font-size: 12px; font-style: italic; flex: 0 0 auto; }
.sm-tree > .sm-node > .sm-row > .sm-link { font-family: "Playfair Display", serif; font-weight: 600; color: var(--brick-dark); font-size: 18px; padding: 6px 10px; }
.sm-tree > .sm-node { padding: 6px 0; border-bottom: 1px dotted var(--line); }
.sm-tree > .sm-node:last-child { border-bottom: none; }
.sm-node.sm-has-children > .sm-children { display: none; }
.sm-node.sm-open > .sm-children { display: block; }
.sm-node.sm-filtered-out { display: none; }
.sm-link mark { background: var(--gold-soft); color: var(--ink); padding: 0 2px; border-radius: 2px; }
.sm-empty { padding: 20px; color: var(--ink-mute); font-style: italic; text-align: center; }

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .bento { grid-template-columns: repeat(4, 1fr); grid-auto-rows: 160px; }
  .bento__tile--hero   { grid-column: span 4; grid-row: span 2; }
  .bento__tile--tall   { grid-column: span 2; grid-row: span 2; }
  .bento__tile--wide   { grid-column: span 4; }
  .bento__tile--regular{ grid-column: span 2; }
  .story { grid-template-columns: 1fr; gap: 40px; }
  .story__media { aspect-ratio: 5/3; max-width: 720px; margin: 0 auto; }
  .visit { grid-template-columns: 1fr; gap: 32px; }
  .explore-grid { grid-template-columns: repeat(2, 1fr); }
  .edu-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
  .visit-info { grid-template-columns: 1fr; }
  .transport-grid, .amenities-grid { grid-template-columns: repeat(2, 1fr); }
  .tour-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .section { padding: 60px 0; }
  .top-announce .announce-items { gap: 14px; font-size: 12px; }
  .top-announce .announce-items span:nth-child(n+3) { display: none; }
  .main-nav { display: none; position: absolute; top: 100%; left: 0; right: 0; background: #fff; flex-direction: column; align-items: stretch; gap: 0; padding: 8px 16px 14px; border-bottom: 1px solid var(--line); box-shadow: var(--shadow-md); }
  .main-nav.is-open { display: flex; }
  .main-nav a { padding: 12px; border-radius: 6px; }
  .nav-cta { margin: 6px 0 0 !important; align-self: flex-start; }
  .menu-toggle { display: inline-flex; }
  .hero { min-height: 520px; }
  .hero__content { padding: 88px 24px 96px; }
  .quickbar { margin-top: -40px; }
  .quickbar__card { grid-template-columns: repeat(2, 1fr); padding: 0; }
  .quickbar__item { border-right: 0; border-bottom: 1px solid var(--line-soft); padding: 16px 16px; }
  .quickbar__item:nth-child(odd) { border-right: 1px solid var(--line-soft); }
  .quickbar__item:nth-last-child(-n+2) { border-bottom: 0; }
  .bento { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 160px; }
  .bento__tile--hero, .bento__tile--tall, .bento__tile--wide, .bento__tile--regular { grid-column: span 2; }
  .explore-grid, .edu-grid, .activities, .multi { grid-template-columns: 1fr; }
  .multi__item { border-right: 0; border-bottom: 1px solid var(--line-soft); }
  .multi__item:last-child { border-bottom: 0; }
  .footer-grid { grid-template-columns: 1fr; gap: 32px; }
  .precinct-list { grid-template-columns: repeat(2, 1fr); }
  .story__facts { grid-template-columns: 1fr; gap: 14px; }
  .activity { padding: 28px 24px; }
  article.article-body { padding: 0 4px; }
  article.article-body p:first-of-type::first-letter { font-size: 2.4em; padding: 4px 8px 0 0; }
  .visit-hero { min-height: 360px; }
  .visit-hero__content { padding: 64px 0 40px; }
  .info-card { padding: 22px 20px; }
  .transport-grid, .amenities-grid { grid-template-columns: 1fr 1fr; }
  .directions-map iframe { height: 320px; }
  .booking-section { padding: 28px 22px; }
  .service-row { grid-template-columns: auto 1fr; gap: 14px; padding: 18px 20px; }
  .service-row__cta {
    grid-column: 1 / -1;
    flex-direction: row; align-items: center; justify-content: space-between;
    border-left: 0; border-top: 1px solid var(--line);
    padding: 12px 0 0; padding-left: 0; margin-top: 4px;
  }
  .rules-highlight {
    grid-template-columns: 1fr; text-align: center; justify-items: center;
    padding: 24px 22px; gap: 16px;
  }
  .a11y-banner { flex-direction: column; text-align: center; align-items: center; }
  .rule-item { grid-template-columns: 1fr; gap: 12px; padding: 24px 0; }
  .rule-item__number { text-align: left; font-size: 48px; padding-top: 0; }
  .emergency-card { grid-template-columns: 1fr; text-align: center; padding: 28px 24px; gap: 18px; }
  .emergency-card__icon { margin: 0 auto; }
  .emergency-card__numbers { flex-direction: row; justify-content: center; flex-wrap: wrap; }
  .rules-hero__tabs { margin-top: 22px; max-width: 100%; overflow-x: auto; }
  .lang-tab { padding: 7px 14px; font-size: 12px; white-space: nowrap; }
}
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
  html { scroll-behavior: auto; }
}
"""


# =========================================================================
# PAGE TEMPLATE
# =========================================================================
NAV_ITEMS = [
    ("/di-tich/", "Di tích"),
    ("/tham-quan/", "Tham quan"),
    ("/hoat-dong/", "Hoạt động"),
    ("/giao-duc-di-san/", "Giáo dục di sản"),
    ("/ve-chung-toi/", "Về chúng tôi"),
]

ICON_CLOCK  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_PIN    = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_PHONE  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_TICKET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"/><path d="M4 6v12c0 1.1.9 2 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/></svg>'
ICON_MAIL   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
ICON_ARROW  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'


def _nav_html(current_path: str) -> str:
    parts = []
    for href, label in NAV_ITEMS:
        active = " active" if current_path.startswith(href) else ""
        parts.append(f'<a href="{href}" class="{active.strip()}">{escape(label)}</a>')
    parts.append('<a href="#mua-ve" class="nav-cta">Đặt vé</a>')
    return "\n".join(parts)


def _breadcrumbs_html(breadcrumbs):
    if not breadcrumbs:
        return ""
    parts = []
    for href, label in breadcrumbs:
        if href:
            parts.append(f'<a href="{href}">{escape(label)}</a>')
        else:
            parts.append(f'<span>{escape(label)}</span>')
    sep = '<span class="sep">›</span>'
    return f'<div class="breadcrumbs"><div class="container">{sep.join(parts)}</div></div>'


def page(title: str, body: str, current_path: str = "/", breadcrumbs=None) -> str:
    nav = _nav_html(current_path)
    bc = _breadcrumbs_html(breadcrumbs)
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} — Văn Miếu Quốc Tử Giám</title>
<meta name="description" content="Văn Miếu – Quốc Tử Giám · Di tích Quốc gia đặc biệt · Trường đại học đầu tiên của Việt Nam · 82 Bia Tiến sĩ được UNESCO công nhận.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>

<div class="top-announce">
  <div class="container">
    <div class="announce-items">
      <span>{ICON_CLOCK} Mở cửa hôm nay · 07:30 – 18:00</span>
      <span>{ICON_PIN} 58 Quốc Tử Giám, Đống Đa, Hà Nội</span>
      <span>{ICON_PHONE} 024.3747.1322</span>
    </div>
    <div class="lang-pick">
      <a href="#" class="is-active">VI</a>
      <a href="#">EN</a>
      <a href="#">FR</a>
    </div>
  </div>
</div>

<header class="site-header">
  <div class="container">
    <a class="brand" href="/">
      <span class="brand-mark">VM</span>
      <span class="brand-text">
        <span class="name">Văn Miếu – Quốc Tử Giám</span>
        <span class="sub">Di tích Quốc gia đặc biệt</span>
      </span>
    </a>
    <nav class="main-nav" id="mainNav">
      {nav}
    </nav>
    <button class="menu-toggle" aria-label="Mở menu" aria-expanded="false" aria-controls="mainNav">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>
{bc}
<main>
{body}
</main>

<footer class="site-footer" id="mua-ve">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">
          <span class="brand-mark">VM</span>
          <span class="brand-text">
            <span class="name">Văn Miếu – Quốc Tử Giám</span>
            <span class="sub">Di tích Quốc gia đặc biệt</span>
          </span>
        </a>
        <p>Trung tâm Hoạt động Văn hoá Khoa học Văn Miếu – Quốc Tử Giám là đơn vị trực thuộc Sở Văn hoá và Thể thao Hà Nội, có chức năng quản lý và phát huy giá trị di tích.</p>
        <div class="footer-contact">
          <span>{ICON_PIN} 58 Phố Quốc Tử Giám, Đống Đa, Hà Nội</span>
          <span>{ICON_PHONE} 024.3747.1322 · 024.3211.5793</span>
          <span>{ICON_MAIL} vanmieuqtg@hanoi.gov.vn</span>
        </div>
      </div>
      <div class="footer-col">
        <h4>Tham quan</h4>
        <ul>
          <li><a href="/tham-quan/">Thông tin tham quan</a></li>
          <li><a href="/tham-quan/">Giờ mở cửa · giá vé</a></li>
          <li><a href="/tham-quan/">Nội quy tham quan</a></li>
          <li><a href="/tham-quan/">Dịch vụ &amp; tiện ích</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Khám phá</h4>
        <ul>
          <li><a href="/di-tich/">Di tích</a></li>
          <li><a href="/hoat-dong/">Hoạt động</a></li>
          <li><a href="/giao-duc-di-san/">Giáo dục di sản</a></li>
          <li><a href="/ve-chung-toi/">Về chúng tôi</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Kết nối</h4>
        <ul>
          <li><a href="#">Facebook</a></li>
          <li><a href="#">YouTube</a></li>
          <li><a href="#">TripAdvisor</a></li>
          <li><a href="/so-do-trang/">Sơ đồ trang</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 Trung tâm Hoạt động Văn hoá Khoa học Văn Miếu – Quốc Tử Giám</div>
      <div class="legal">
        <a href="#">Chính sách bảo mật</a>
        <a href="#">Điều khoản sử dụng</a>
      </div>
    </div>
  </div>
</footer>

<div class="lightbox" id="lb" aria-hidden="true">
  <span class="close" id="lb-close">×</span>
  <span class="nav prev" id="lb-prev">‹</span>
  <img id="lb-img" alt="">
  <span class="nav next" id="lb-next">›</span>
  <span class="counter" id="lb-counter"></span>
</div>
<script>
(function(){{
  var btn = document.querySelector('.menu-toggle');
  var nav = document.getElementById('mainNav');
  if (btn && nav) {{
    btn.addEventListener('click', function(){{
      var open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }});
  }}
  var lb = document.getElementById('lb');
  var img = document.getElementById('lb-img');
  var counter = document.getElementById('lb-counter');
  var links = []; var idx = 0;
  function collect(){{ links = Array.from(document.querySelectorAll('.gallery a[href]')); }}
  function open(i){{ idx = (i + links.length) % links.length; img.src = links[idx].getAttribute('href'); counter.textContent = (idx+1)+' / '+links.length; lb.classList.add('open'); lb.setAttribute('aria-hidden','false'); document.body.style.overflow = 'hidden'; }}
  function close(){{ lb.classList.remove('open'); lb.setAttribute('aria-hidden','true'); img.src = ''; document.body.style.overflow = ''; }}
  document.addEventListener('click', function(e){{ var a = e.target.closest('.gallery a[href]'); if (a) {{ e.preventDefault(); collect(); open(links.indexOf(a)); }} }});
  var cb = document.getElementById('lb-close'); if (cb) cb.onclick = close;
  var pb = document.getElementById('lb-prev'); if (pb) pb.onclick = function(e){{ e.stopPropagation(); open(idx-1); }};
  var nb = document.getElementById('lb-next'); if (nb) nb.onclick = function(e){{ e.stopPropagation(); open(idx+1); }};
  if (lb) lb.onclick = function(e){{ if (e.target === lb || e.target === img) close(); }};
  document.addEventListener('keydown', function(e){{ if (!lb || !lb.classList.contains('open')) return; if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') open(idx-1); else if (e.key === 'ArrowRight') open(idx+1); }});
}})();
</script>
</body></html>"""


# =========================================================================
# RENDERERS — Article, Listing, Hub, Program
# =========================================================================
def _img_anchor(img: str, captions: dict) -> str:
    thumb = vm.thumb_for(img)
    caption = captions.get(img, "") if captions else ""
    if caption:
        return (
            f'<a href="{img}" title="{escape(caption)}">'
            f'<img src="{thumb}" loading="lazy" alt="{escape(caption)}">'
            f'<span class="caption">{escape(caption)}</span></a>'
        )
    return f'<a href="{img}"><img src="{thumb}" loading="lazy" alt=""></a>'


def render_article(art, breadcrumbs=None):
    body_parts = [art.content_vi or ""]
    if art.images:
        gallery = "\n".join(_img_anchor(img, art.captions) for img in art.images)
        body_parts.append(
            f'<h3>Hình ảnh</h3><div class="gallery">{gallery}</div>'
        )

    extra_lang = ""
    if art.content_en:
        extra_lang += (
            f'<details class="lang-block">'
            f'<summary>English version</summary>'
            f'<h2>{escape(art.title_en or art.title_vi)}</h2>'
            f'{art.content_en}</details>'
        )
    if art.content_fr:
        extra_lang += (
            f'<details class="lang-block">'
            f'<summary>Version française</summary>'
            f'{art.content_fr}</details>'
        )

    return f"""
<div class="page-body">
  <div class="container">
    <article class="article-body">
      <span class="article-meta">Bài viết · Văn Miếu – Quốc Tử Giám</span>
      <h1>{escape(art.title_vi)}</h1>
      {"".join(body_parts)}
      {extra_lang}
    </article>
  </div>
</div>
"""


def render_listing(title: str, intro: str, items, base_path: str):
    cards = []
    for slug, t, ex, thumb in items:
        if thumb:
            thumb_html = f'<div class="thumb" style="background-image:url(\'{thumb}\')"></div>'
        else:
            initial = escape((t or "V")[:1].upper())
            thumb_html = f'<div class="thumb thumb--empty">{initial}</div>'
        cards.append(f"""
<a class="card" href="{base_path}{slug}/">
  {thumb_html}
  <div class="body">
    <h3>{escape(t)}</h3>
    <p>{escape(ex)}</p>
    <span class="more">Xem chi tiết {ICON_ARROW}</span>
  </div>
</a>""")
    return f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Mục lục</span>
    <h1>{escape(title)}</h1>
    <p class="lede">{escape(intro)}</p>
  </div>
</section>
<div class="page-body">
  <div class="container">
    <div class="grid">{"".join(cards)}</div>
  </div>
</div>
"""


def render_section_index(title: str, intro: str, sections):
    cards = []
    for href, t, count, blurb in sections:
        cards.append(f"""
<a class="hub-card" href="{href}">
  <span class="hub-card__count">{count} bài viết</span>
  <h3>{escape(t)}</h3>
  <p>{escape(blurb)}</p>
  <span class="hub-card__more">Khám phá {ICON_ARROW}</span>
</a>""")
    return f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Chuyên mục</span>
    <h1>{escape(title)}</h1>
    <p class="lede">{escape(intro)}</p>
  </div>
</section>
<div class="page-body">
  <div class="container">
    <div class="hub-grid">{"".join(cards)}</div>
  </div>
</div>
"""


def render_program(p):
    parts = [
        '<div class="page-body"><div class="container">',
        '<article class="article-body">',
        '<span class="article-meta">Chương trình giáo dục di sản</span>',
        f'<h1>{escape(p["title"])}</h1>',
    ]

    if p.get("main"):
        for d in p["main"]:
            parts.append(f'<h3>{escape(d["label"])}</h3>{d["html"]}')
    if p.get("pre"):
        parts.append('<h2 style="margin-top:44px;padding-top:24px;border-top:1px solid var(--line);">Trước thăm quan</h2>')
        for d in p["pre"]:
            parts.append(f'<h3>{escape(d["label"])}</h3>{d["html"]}')
    if p.get("post"):
        parts.append('<h2 style="margin-top:44px;padding-top:24px;border-top:1px solid var(--line);">Sau thăm quan</h2>')
        for d in p["post"]:
            parts.append(f'<h3>{escape(d["label"])}</h3>{d["html"]}')

    if p.get("images"):
        gallery = "\n".join(_img_anchor(img, p.get("captions", {})) for img in p["images"])
        parts.append(f'<h3>Hình ảnh chương trình</h3><div class="gallery">{gallery}</div>')

    parts.append("</article></div></div>")
    return "".join(parts)


# =========================================================================
# HOMEPAGE
# =========================================================================
def _pick_hero_image():
    """Pick a hero image from the freshly-generated /assets/images tree."""
    if not vm.IMG_DIR.exists():
        return None
    candidates = list(vm.IMG_DIR.rglob("*.jpg"))
    if not candidates:
        return None
    # prefer full (not thumb) panoramic / iconic shots
    for c in candidates:
        n = c.name.lower()
        if "-thumb" in n:
            continue
        if "toan-canh" in n or "kvc" in n or "khue" in n or "1-toan-canh" in n:
            return c
    for c in candidates:
        if "-thumb" not in c.name.lower():
            return c
    return candidates[0]


def _rel_img_url(path: Path) -> str:
    """Return /assets/images/... URL for an image under IMG_DIR."""
    try:
        rel = path.relative_to(vm.SITE)
    except ValueError:
        return ""
    return "/" + str(rel).replace(os.sep, "/")


def _find_image(*keywords):
    """Find first image whose filename contains ALL given keywords (non-thumb)."""
    if not vm.IMG_DIR.exists():
        return ""
    for img in vm.IMG_DIR.rglob("*.jpg"):
        n = img.name.lower()
        if "-thumb" in n:
            continue
        if all(k in n for k in keywords):
            return _rel_img_url(img)
    return ""


def build_home():
    # Copy hero image into /assets/images/hero.jpg (same trick as old site)
    hero = _pick_hero_image()
    hero_url = "/assets/images/hero.jpg"
    if hero:
        import shutil
        shutil.copy2(hero, vm.IMG_DIR / "hero.jpg")

    # Pick iconic bento images dynamically
    img_kvc         = _find_image("kvc", "gieng") or _find_image("kvc") or _find_image("khue")
    img_bia         = _find_image("vuon-bia") or _find_image("bia-tien-si")
    img_dai_thanh   = _find_image("cong-dai-thanh") or _find_image("dai-thanh")
    img_thai_hoc    = _find_image("cong-thai-hoc") or _find_image("thai-hoc")
    img_rong        = _find_image("rong") or _find_image("mai-dien")
    img_ho_van      = _find_image("ho-van")
    img_story       = _find_image("toan-canh") or _find_image("1-toan-canh") or hero_url

    body = f"""
<section class="hero">
  <div class="hero__media" role="img" aria-label="Toàn cảnh Văn Miếu – Quốc Tử Giám"
       style="background:
         linear-gradient(180deg, rgba(28,25,23,.25) 0%, rgba(28,25,23,.55) 70%, rgba(28,25,23,.72) 100%),
         url('{hero_url}') center/cover no-repeat;">
  </div>
  <div class="hero__content">
    <div class="hero__kicker">Di tích Quốc gia đặc biệt · 1070</div>
    <h1 class="display">Văn Miếu – <em>Quốc Tử Giám</em></h1>
    <p class="hero__lede">Trường đại học đầu tiên của Việt Nam — gần một nghìn năm gìn giữ tinh hoa đạo học và văn hiến Thăng Long – Hà Nội.</p>
    <div class="hero__ctas">
      <a href="#mua-ve" class="btn btn--primary">Đặt vé tham quan {ICON_ARROW}</a>
      <a href="#kham-pha" class="btn btn--ghost">Khám phá di tích</a>
    </div>
  </div>
  <div class="hero__scroll" aria-hidden="true">
    <span>Cuộn xuống</span><span class="arrow"></span>
  </div>
</section>

<div class="container quickbar">
  <div class="quickbar__card">
    <div class="quickbar__item">
      <div class="quickbar__icon">{ICON_CLOCK}</div>
      <div>
        <div class="quickbar__label">Giờ mở cửa</div>
        <div class="quickbar__value">07:30 – 18:00</div>
        <div class="quickbar__meta">Mùa hè · 08:00–17:00 mùa đông</div>
      </div>
    </div>
    <div class="quickbar__item">
      <div class="quickbar__icon">{ICON_TICKET}</div>
      <div>
        <div class="quickbar__label">Giá vé</div>
        <div class="quickbar__value">30.000đ / người lớn</div>
        <div class="quickbar__meta">15.000đ HS/SV · miễn phí dưới 15 tuổi</div>
      </div>
    </div>
    <div class="quickbar__item">
      <div class="quickbar__icon">{ICON_PIN}</div>
      <div>
        <div class="quickbar__label">Địa chỉ</div>
        <div class="quickbar__value">58 Quốc Tử Giám</div>
        <div class="quickbar__meta">P. Văn Miếu, Đống Đa, Hà Nội</div>
      </div>
    </div>
    <div class="quickbar__item">
      <div class="quickbar__icon">{ICON_PHONE}</div>
      <div>
        <div class="quickbar__label">Liên hệ</div>
        <div class="quickbar__value">024.3747.1322</div>
        <div class="quickbar__meta">vanmieuqtg@hanoi.gov.vn</div>
      </div>
    </div>
  </div>
</div>

<section class="section section--paper" id="cau-chuyen">
  <div class="container">
    <div class="story">
      <div class="story__body">
        <span class="eyebrow">Câu chuyện di sản</span>
        <h2 class="section-title">Gần một nghìn năm đạo học và văn hiến</h2>
        <p><strong>Năm 1070</strong>, vua Lý Thánh Tông cho xây dựng Văn Miếu thờ Khổng Tử cùng các bậc Tiên Nho. Sáu năm sau, <strong>Quốc Tử Giám</strong> được thành lập bên cạnh — trường đại học đầu tiên của Việt Nam, đào tạo hàng vạn Nho sĩ và 1.304 vị Tiến sĩ trong suốt tám thế kỷ.</p>
        <blockquote class="story__pullquote">
          “Hiền tài là nguyên khí của quốc gia, nguyên khí thịnh thì thế nước mạnh mà hưng thịnh.”
          <span style="display:block;font-style:normal;font-size:13px;color:var(--ink-mute);margin-top:10px;letter-spacing:.05em;">— Thân Nhân Trung, 1484</span>
        </blockquote>
        <p>Ngày nay, quần thể di tích là <strong>Di tích Quốc gia đặc biệt</strong> với <strong>82 bia Tiến sĩ</strong> được UNESCO công nhận là <em>Di sản Tư liệu Thế giới</em> — nơi lưu giữ ký ức khoa cử và tinh thần hiếu học của dân tộc Việt Nam.</p>
        <div class="story__facts">
          <div class="fact"><div class="fact__number">1070</div><div class="fact__label">Năm khởi dựng</div></div>
          <div class="fact"><div class="fact__number">82</div><div class="fact__label">Bia Tiến sĩ · Di sản Tư liệu Thế giới</div></div>
          <div class="fact"><div class="fact__number">1.304</div><div class="fact__label">Vị Tiến sĩ được khắc tên</div></div>
        </div>
      </div>
      <div class="story__media">
        <img src="{img_story}" alt="Toàn cảnh Văn Miếu – Quốc Tử Giám" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="section section--cream" id="kham-pha">
  <div class="container">
    <span class="eyebrow">Khám phá</span>
    <h2 class="section-title">Những điểm đến biểu tượng</h2>
    <p class="section-lede">Sáu công trình tiêu biểu trong quần thể Văn Miếu – Quốc Tử Giám, mỗi nơi gìn giữ một lớp ký ức của gần một nghìn năm lịch sử.</p>
    <div class="bento">
      <a class="bento__tile bento__tile--hero" href="/di-tich/kien-truc/" style="background-image:url('{img_kvc}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">Kiến trúc · Biểu tượng</div>
          <h3 class="bento__title">Khuê Văn Các &amp; Giếng Thiên Quang</h3>
          <p class="bento__desc">Lầu "sao Khuê chiếu sáng" bên hồ vuông — biểu tượng của Thủ đô Hà Nội.</p>
        </div>
      </a>
      <a class="bento__tile bento__tile--tall" href="/di-tich/bia-tien-si/" style="background-image:url('{img_bia}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">UNESCO · 2011</div>
          <h3 class="bento__title">82 Bia Tiến sĩ</h3>
          <p class="bento__desc">Di sản Tư liệu Thế giới ghi tên 1.304 Tiến sĩ khoa cử Việt Nam.</p>
        </div>
      </a>
      <a class="bento__tile bento__tile--regular" href="/di-tich/kien-truc/" style="background-image:url('{img_dai_thanh}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">Kiến trúc</div>
          <h3 class="bento__title">Đại Thành Môn</h3>
          <p class="bento__desc">Cổng dẫn vào điện thờ Khổng Tử.</p>
        </div>
      </a>
      <a class="bento__tile bento__tile--regular" href="/di-tich/kien-truc/" style="background-image:url('{img_thai_hoc}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">Kiến trúc</div>
          <h3 class="bento__title">Nhà Thái Học</h3>
          <p class="bento__desc">Giảng đường xưa của các vị Tế tửu – Tư nghiệp.</p>
        </div>
      </a>
      <a class="bento__tile bento__tile--wide" href="/di-tich/tuong-tho/" style="background-image:url('{img_rong}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">Tín ngưỡng · Thờ tự</div>
          <h3 class="bento__title">Hệ thống tượng thờ Tứ Phối</h3>
          <p class="bento__desc">Khổng Tử, Nhan Tử, Tăng Tử, Tử Tư và Mạnh Tử — các bậc Thánh của Nho giáo.</p>
        </div>
      </a>
      <a class="bento__tile bento__tile--wide" href="/di-tich/kien-truc/" style="background-image:url('{img_ho_van}')">
        <span class="bento__arrow">{ICON_ARROW}</span>
        <div class="bento__inner">
          <div class="bento__kicker">Cảnh quan</div>
          <h3 class="bento__title">Hồ Văn &amp; Gò Kim Châu</h3>
          <p class="bento__desc">Gò đảo ngự trước Văn Miếu — nơi các sĩ tử xưa bình văn.</p>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper" id="tham-quan-home">
  <div class="container">
    <span class="eyebrow">Kế hoạch tham quan</span>
    <h2 class="section-title">Một hành trình qua năm lớp cổng</h2>
    <p class="section-lede">Quần thể nội tự được chia thành năm khu vực nối tiếp nhau theo trục Bắc – Nam, mỗi khu một ý nghĩa riêng trong hành trình giáo dưỡng của người xưa.</p>
    <div class="visit">
      <div class="visit__map" aria-hidden="true">
        <div class="visit__map-illustration">
          <svg class="visit__map-svg" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="hatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="6" stroke="#c9a14a" stroke-opacity=".22" stroke-width="1"/>
              </pattern>
            </defs>
            <rect x="80" y="20" width="240" height="260" rx="4" fill="#fffbec" stroke="#8b2e2e" stroke-width="2"/>
            <rect x="80" y="20"  width="240" height="52" fill="url(#hatch)" stroke="#c9a14a" stroke-opacity=".55"/>
            <rect x="80" y="72"  width="240" height="52" fill="#f5efe2" stroke="#c9a14a" stroke-opacity=".55"/>
            <rect x="80" y="124" width="240" height="52" fill="#fffbec" stroke="#c9a14a" stroke-opacity=".55"/>
            <rect x="80" y="176" width="240" height="52" fill="#f5efe2" stroke="#c9a14a" stroke-opacity=".55"/>
            <rect x="80" y="228" width="240" height="52" fill="url(#hatch)" stroke="#c9a14a" stroke-opacity=".55"/>
            <g transform="translate(200, 100)"><circle r="10" fill="#8b2e2e"/><circle r="5" fill="#c9a14a"/></g>
            <rect x="180" y="138" width="40" height="28" fill="#cfe0de" stroke="#5a7a78"/>
            <g fill="#8b2e2e" opacity=".7">
              <rect x="110" y="146" width="4" height="10"/><rect x="118" y="146" width="4" height="10"/>
              <rect x="126" y="146" width="4" height="10"/><rect x="134" y="146" width="4" height="10"/>
              <rect x="142" y="146" width="4" height="10"/><rect x="150" y="146" width="4" height="10"/>
              <rect x="110" y="160" width="4" height="10"/><rect x="118" y="160" width="4" height="10"/>
              <rect x="126" y="160" width="4" height="10"/><rect x="134" y="160" width="4" height="10"/>
              <rect x="142" y="160" width="4" height="10"/><rect x="150" y="160" width="4" height="10"/>
              <rect x="254" y="146" width="4" height="10"/><rect x="262" y="146" width="4" height="10"/>
              <rect x="270" y="146" width="4" height="10"/><rect x="278" y="146" width="4" height="10"/>
              <rect x="286" y="146" width="4" height="10"/>
              <rect x="254" y="160" width="4" height="10"/><rect x="262" y="160" width="4" height="10"/>
              <rect x="270" y="160" width="4" height="10"/><rect x="278" y="160" width="4" height="10"/>
              <rect x="286" y="160" width="4" height="10"/>
            </g>
            <rect x="170" y="194" width="60" height="18" fill="#8b2e2e" opacity=".8"/>
            <polygon points="170,194 200,182 230,194" fill="#5a1818"/>
            <rect x="160" y="248" width="80" height="22" fill="#8b2e2e" opacity=".7"/>
            <polygon points="160,248 200,234 240,248" fill="#5a1818"/>
            <g transform="translate(345, 30)">
              <circle r="14" fill="#fff" stroke="#c9a14a"/>
              <text y="4" text-anchor="middle" font-size="12" font-family="Playfair Display, serif" fill="#8b2e2e" font-weight="700">N</text>
            </g>
            <text x="200" y="296" text-anchor="middle" font-size="10" fill="#8b2e2e" font-weight="600" letter-spacing="2">CỔNG VÀO</text>
          </svg>
        </div>
      </div>
      <div class="visit__tips">
        <h3>Thông tin cho du khách</h3>
        <ul>
          <li><strong>Giờ mở cửa</strong><span>07:30 – 18:00 (mùa hè) · 08:00 – 17:00 (mùa đông)</span></li>
          <li><strong>Giá vé</strong><span>30.000đ người lớn · 15.000đ HS/SV &amp; người &gt;60 · Miễn phí trẻ &lt;15</span></li>
          <li><strong>Thời gian tham quan</strong><span>Đề xuất 60 – 90 phút cho toàn bộ năm khu nội tự</span></li>
          <li><strong>Thuyết minh viên</strong><span>Việt · Anh · Trung · Pháp — đặt qua 024.3823.5601</span></li>
          <li><strong>Thuyết minh tự động</strong><span>8 ngôn ngữ · 30.000đ (VI) · 50.000đ (ngoại ngữ)</span></li>
          <li><strong>Tiện ích</strong><span>Bãi đỗ ô tô · bãi xe máy vườn Giám · café · hàng ăn · lưu niệm</span></li>
        </ul>
        <div class="visit__cta">
          <a href="#mua-ve" class="btn btn--primary">Đặt vé trực tuyến {ICON_ARROW}</a>
          <a href="/tham-quan/" class="btn btn--light">Xem thêm thông tin</a>
        </div>
      </div>
    </div>
    <div class="precinct-list" aria-label="Năm khu vực nội tự">
      <div class="precinct"><h4>Nhập Đạo – Thành Đạt</h4><p>Từ Văn Miếu Môn đến Đại Trung Môn</p></div>
      <div class="precinct"><h4>Thành Đạt – Súc Văn</h4><p>Tứ trụ &amp; Đại Trung Môn</p></div>
      <div class="precinct"><h4>Khuê Văn Các</h4><p>Giếng Thiên Quang &amp; 82 bia Tiến sĩ</p></div>
      <div class="precinct"><h4>Đại Thành</h4><p>Điện thờ Khổng Tử &amp; Tứ Phối</p></div>
      <div class="precinct"><h4>Thái Học</h4><p>Giảng đường Quốc Tử Giám xưa</p></div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <span class="eyebrow">Tư liệu &amp; Nghiên cứu</span>
    <h2 class="section-title">Khám phá di sản theo chủ đề</h2>
    <p class="section-lede">Đi sâu vào lịch sử, kiến trúc, hiện vật và những con người làm nên tinh thần của Văn Miếu – Quốc Tử Giám.</p>
    <div class="explore-grid">
      <a class="explore-card" href="/di-tich/lich-su/">
        <div class="explore-card__media" style="background-image:url('{img_story}')"></div>
        <div class="explore-card__body">
          <span class="explore-card__kicker">5 thời kỳ</span>
          <h3 class="explore-card__title">Lịch sử qua các triều đại</h3>
          <p class="explore-card__desc">Từ Lý – Trần – Hồ đến Lê sơ – Mạc, Lê Trung hưng và giai đoạn hiện đại (1945 – nay).</p>
          <span class="explore-card__more">Xem dòng thời gian {ICON_ARROW}</span>
        </div>
      </a>
      <a class="explore-card" href="/di-tich/bia-tien-si/">
        <div class="explore-card__media" style="background-image:url('{img_bia}')"></div>
        <div class="explore-card__body">
          <span class="explore-card__kicker">Di sản Tư liệu Thế giới</span>
          <h3 class="explore-card__title">82 Bia Tiến sĩ</h3>
          <p class="explore-card__desc">Ghi danh 1.304 vị khoa cử qua 82 khoa thi từ 1442 đến 1779 — ký ức vàng son của Nho học Việt Nam.</p>
          <span class="explore-card__more">Duyệt bia tiến sĩ {ICON_ARROW}</span>
        </div>
      </a>
      <a class="explore-card" href="/di-tich/danh-nhan/">
        <div class="explore-card__media" style="background-image:url('{img_thai_hoc}')"></div>
        <div class="explore-card__body">
          <span class="explore-card__kicker">Danh nhân khoa bảng</span>
          <h3 class="explore-card__title">Những bậc hiền tài</h3>
          <p class="explore-card__desc">Tế tửu – Tư nghiệp Quốc Tử Giám, các vị Tiến sĩ và dòng họ khoa bảng tiêu biểu trong lịch sử Việt Nam.</p>
          <span class="explore-card__more">Gặp gỡ danh nhân {ICON_ARROW}</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper" id="giao-duc">
  <div class="container">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:24px;margin-bottom:40px;">
      <div>
        <span class="eyebrow">Giáo dục di sản</span>
        <h2 class="section-title">Học qua di sản — vui cùng di tích</h2>
        <p class="section-lede" style="margin-bottom:0;">Các chương trình giáo dục dành riêng cho từng lứa tuổi, giúp học sinh tiếp cận di sản theo cách phù hợp và hấp dẫn nhất.</p>
      </div>
      <a href="/giao-duc-di-san/" class="btn btn--light">Xem tất cả chương trình {ICON_ARROW}</a>
    </div>
    <div class="edu-grid">
      <a class="edu-card" href="/giao-duc-di-san/mam-non/">
        <div class="edu-card__age">03+</div><div class="edu-card__sub">Mầm non</div>
        <h4>Khám phá qua hình tượng &amp; trò chơi</h4>
        <p>Đi tìm linh vật · Ô kìa con Nghê · Mãnh hổ hạ sơn — làm quen di sản bằng thị giác và trò chơi.</p>
        <span class="edu-card__count">3 chương trình →</span>
      </a>
      <a class="edu-card" href="/giao-duc-di-san/lop-1-3/">
        <div class="edu-card__age">6–8</div><div class="edu-card__sub">Lớp 1 – 3</div>
        <h4>Khám phá Khuê Văn Các &amp; lớp học xưa</h4>
        <p>Tìm hiểu Khuê Văn Các, bia Tiến sĩ và không gian học đường truyền thống của người Việt.</p>
        <span class="edu-card__count">6 chương trình →</span>
      </a>
      <a class="edu-card" href="/giao-duc-di-san/lop-4-6/">
        <div class="edu-card__age">9–11</div><div class="edu-card__sub">Lớp 4 – 6</div>
        <h4>Kiến trúc &amp; biểu tượng văn hoá</h4>
        <p>Đi sâu vào kiến trúc nội thất, linh vật và các giá trị biểu tượng của di tích.</p>
        <span class="edu-card__count">5 chương trình →</span>
      </a>
      <a class="edu-card" href="/giao-duc-di-san/lop-7-12/">
        <div class="edu-card__age">12+</div><div class="edu-card__sub">Lớp 7 – 12</div>
        <h4>Khoa cử, lịch sử &amp; tư liệu gốc</h4>
        <p>Thi Hương – Hội – Đình, Vinh quy bái tổ, sách học &amp; ván khắc, Quốc Tử Giám ở Thăng Long…</p>
        <span class="edu-card__count">10 chương trình →</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--cream" id="hoat-dong">
  <div class="container">
    <span class="eyebrow">Hoạt động &amp; Sự kiện</span>
    <h2 class="section-title">Di sản sống động mỗi ngày</h2>
    <p class="section-lede">Các trưng bày thường xuyên, triển lãm chuyên đề và hoạt động văn hoá định kỳ tại khuôn viên Văn Miếu – Quốc Tử Giám.</p>
    <div class="activities">
      <div class="activity activity--featured">
        <span class="activity__tag"><svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="6"/></svg> Đang diễn ra</span>
        <h3>Trưng bày thường xuyên</h3>
        <p>Không gian trưng bày về lịch sử hình thành, kiến trúc và các giá trị văn hoá của Văn Miếu – Quốc Tử Giám, kèm theo bộ sưu tập ảnh tư liệu quý hiếm.</p>
        <a href="/hoat-dong/" class="btn btn--light" style="background:#fff;color:var(--brick);">Xem trưng bày {ICON_ARROW}</a>
      </div>
      <div class="activity">
        <span class="activity__tag">Sự kiện định kỳ</span>
        <h3>Triển lãm chuyên đề &amp; hoạt động văn hoá</h3>
        <p>Các triển lãm theo chủ đề, hội thảo khoa học, chương trình trình diễn thư pháp, ca trù — cập nhật theo mùa và dịp lễ.</p>
        <a href="/hoat-dong/" class="btn btn--light">Theo dõi lịch {ICON_ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper" id="ngon-ngu">
  <div class="container">
    <div class="multi">
      <div class="multi__item">
        <span class="multi__flag">Tiếng Việt</span>
        <div class="multi__greeting">Xin chào</div>
        <p class="multi__desc">Thông tin đầy đủ, giới thiệu di tích và các bài nghiên cứu chuyên sâu.</p>
        <a href="/" class="multi__link">Vào trang Tiếng Việt →</a>
      </div>
      <div class="multi__item">
        <span class="multi__flag">English</span>
        <div class="multi__greeting">Welcome</div>
        <p class="multi__desc">Essential visitor information and heritage highlights in English.</p>
        <a href="#" class="multi__link">Go to English version →</a>
      </div>
      <div class="multi__item">
        <span class="multi__flag">Français</span>
        <div class="multi__greeting">Bienvenue</div>
        <p class="multi__desc">Informations essentielles pour les visiteurs et points forts du patrimoine.</p>
        <a href="#" class="multi__link">Version française →</a>
      </div>
    </div>
  </div>
</section>
"""
    vm.write_page(vm.SITE / "index.html", page("Trang chủ", body, "/"))


# =========================================================================
# THAM QUAN — rich visitor page (hero + hours/prices + directions +
# amenities + tours + booking + docs)
# =========================================================================

# SVG icon set (Lucide-style, stroke-current)
def _svg(path_d, extra=""):
    return (
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"{extra}>'
        f'{path_d}</svg>'
    )

ICON_BUS       = _svg('<path d="M8 6v6"/><path d="M16 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2v-4.4c0-.4-.1-.8-.2-1.2A92 92 0 0 0 21 3.4 2 2 0 0 0 19.2 2H4.8c-.9 0-1.6.5-1.8 1.4-.3 1-1 3.8-1 3.8a6 6 0 0 0-.2 1.2v4.4c0 .4.1.8.2 1.2L2.8 16H6"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>')
ICON_TRAIN     = _svg('<rect x="4" y="3" width="16" height="16" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><path d="m8 19-2 3"/><path d="m18 22-2-3"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/>')
ICON_CAR       = _svg('<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>')
ICON_TAXI      = _svg('<path d="M10 2h4"/><path d="M5 7h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2z"/><path d="M7 7V4h10v3"/><circle cx="7.5" cy="14.5" r="1.5"/><circle cx="16.5" cy="14.5" r="1.5"/>')
ICON_USER_GUIDE= _svg('<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>')
ICON_HEADPHONE = _svg('<path d="M3 12a9 9 0 0 1 18 0v6a3 3 0 0 1-3 3h-2a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h5"/><path d="M3 18v-6h5a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H6a3 3 0 0 1-3-3z"/>')
ICON_WIFI      = _svg('<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>')
ICON_RESTROOM  = _svg('<path d="M7 4v16"/><path d="M17 4v16"/><path d="M12 4v16"/>')
ICON_COFFEE    = _svg('<path d="M17 8h1a4 4 0 0 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z"/><line x1="6" y1="2" x2="6" y2="4"/><line x1="10" y1="2" x2="10" y2="4"/><line x1="14" y1="2" x2="14" y2="4"/>')
ICON_GIFT      = _svg('<polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>')
ICON_BENCH     = _svg('<path d="M2 9h20"/><path d="M4 9v8"/><path d="M20 9v8"/><path d="M4 13h16"/><path d="M6 17v3"/><path d="M18 17v3"/>')
ICON_MAP_ICON  = _svg('<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>')
ICON_A11Y      = _svg('<circle cx="12" cy="4" r="2"/><path d="M19 13v-2a7 7 0 1 0-14 0v2"/><path d="M15 21a3 3 0 1 0-6 0"/><path d="M12 13v8"/>')
ICON_EXTERNAL  = _svg('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>')
ICON_CHECK     = _svg('<polyline points="20 6 9 17 4 12"/>')
ICON_DOC       = _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>')
ICON_SUNRISE   = _svg('<path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/><polyline points="8 6 12 2 16 6"/>')
ICON_MOON      = _svg('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>')
ICON_LEAF      = _svg('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>')
ICON_FLAME     = _svg('<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>')
ICON_SHIRT     = _svg('<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>')
ICON_BAN       = _svg('<circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>')
ICON_SCALE     = _svg('<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>')
ICON_SHIELD    = _svg('<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>')
ICON_BOOK      = _svg('<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>')
ICON_STAR      = _svg('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>')


NOI_QUY_ICONS = {
    "ticket": ICON_TICKET, "leaf": ICON_LEAF, "flame": ICON_FLAME,
    "shirt": ICON_SHIRT,   "ban": ICON_BAN,   "scale": ICON_SCALE,
    "shield": ICON_SHIELD, "phone": ICON_PHONE,
}

NOI_QUY_L10N = {
    "vi": {
        "label": "Tiếng Việt",
        "kicker": "Nội quy tham quan",
        "h1_pre": "Chào mừng Quý khách đến với",
        "h1_main": "Văn Miếu – Quốc Tử Giám",
        "lede": "Để gìn giữ Di tích Quốc gia đặc biệt và đảm bảo chuyến tham quan trọn vẹn cho mọi người, kính mời Quý khách cùng thực hiện <strong>8 điều sau</strong>.",
        "closing": "Kính chúc Quý khách một chuyến tham quan bổ ích và lý thú.",
        "emergency_eyebrow": "Báo tin khi cần",
        "emergency_h3": "Phát hiện sự việc bất thường?",
        "emergency_p": "Thông báo ngay cho bộ phận bảo vệ di tích qua các số sau.",
        "titles": [
            ("Mua vé & xuất trình",         "ticket"),
            ("Gìn giữ di tích & cảnh quan", "leaf"),
            ("An ninh & phòng cháy",        "flame"),
            ("Trang phục lịch sự",           "shirt"),
            ("Không mê tín · cờ bạc",        "ban"),
            ("Chịu trách nhiệm pháp lý",     "scale"),
            ("Tuân thủ chỉ dẫn bảo vệ",      "shield"),
            ("Báo tin khi phát hiện sự cố",  "phone"),
        ],
    },
    "en": {
        "label": "English",
        "kicker": "Visitor regulations",
        "h1_pre": "Welcome to the Special National Relic",
        "h1_main": "Văn Miếu – Quốc Tử Giám",
        "lede": "To preserve this Special National Relic and ensure a pleasant visit for all, please observe the <strong>8 regulations below</strong>.",
        "closing": "Thank you for your co-operation and have a nice visit.",
        "emergency_eyebrow": "Report incidents",
        "emergency_h3": "Witnessed an incident?",
        "emergency_p": "Please inform the relic's security guards via the numbers below.",
        "titles": [
            ("Purchase & present your ticket", "ticket"),
            ("Protect the relic & landscape",  "leaf"),
            ("Security & fire prevention",     "flame"),
            ("Dress appropriately",            "shirt"),
            ("No superstition · gambling",     "ban"),
            ("Legal responsibility",           "scale"),
            ("Follow security guidance",       "shield"),
            ("Report any incidents",           "phone"),
        ],
    },
    "fr": {
        "label": "Français",
        "kicker": "Règlement du site",
        "h1_pre": "Bienvenue au",
        "h1_main": "Văn Miếu – Quốc Tử Giám",
        "lede": "Pour préserver ce site classé d'intérêt national et assurer une visite agréable à tous, nous vous invitons à respecter les <strong>8 règles suivantes</strong>.",
        "closing": "Merci pour votre coopération et bonne visite !",
        "emergency_eyebrow": "Signaler un incident",
        "emergency_h3": "Vous avez constaté un incident ?",
        "emergency_p": "Veuillez informer les agents de sécurité du site via les numéros ci-dessous.",
        "titles": [
            ("Acheter & présenter le billet", "ticket"),
            ("Respecter le site & le paysage","leaf"),
            ("Sécurité & prévention incendie","flame"),
            ("Tenue appropriée",               "shirt"),
            ("Pas de superstition · jeux",     "ban"),
            ("Responsabilité juridique",       "scale"),
            ("Respecter les consignes",        "shield"),
            ("Signaler tout incident",         "phone"),
        ],
    },
}


def _parse_rules_text(raw: str):
    """Extract up to 8 rule texts from numbered (1.) or bulleted (•) format.
       Works for all three languages: VI/FR use `1.`, EN uses `•`."""
    import re as _re
    rules = []
    line_re = _re.compile(r'^\s*(?:\d{1,2}\.|[•●▪■])\s+(.+?)\s*$')
    for line in raw.splitlines():
        m = line_re.match(line)
        if not m:
            continue
        text = _re.sub(r'\s+', ' ', m.group(1)).strip(' ;.')
        if text:
            rules.append(text)
        if len(rules) == 8:
            break
    return rules


def _render_noi_quy_panel(lang_code: str, raw_text: str, is_active: bool, all_langs) -> str:
    l10n = NOI_QUY_L10N[lang_code]
    rules = _parse_rules_text(raw_text)

    rule_items = ""
    for idx, text in enumerate(rules):
        if idx >= len(l10n["titles"]):
            break
        title, icon_key = l10n["titles"][idx]
        icon = NOI_QUY_ICONS.get(icon_key, ICON_SHIELD)
        rule_items += f"""
<div class="rule-item">
  <div class="rule-item__number">{idx+1:02d}</div>
  <div class="rule-item__content">
    <div class="rule-item__header">
      <span class="rule-item__icon">{icon}</span>
      <h3>{escape(title)}</h3>
    </div>
    <p>{escape(text)}</p>
  </div>
</div>"""

    # Inline tab bar — rendered inside each panel's hero, after the lede.
    tabs_inline = ""
    if len(all_langs) > 1:
        buttons = "".join(
            f'<button type="button" class="lang-tab{ " is-active" if code == lang_code else "" }" data-lang="{code}">{NOI_QUY_L10N[code]["label"]}</button>'
            for code in all_langs
        )
        tabs_inline = f'<div class="rules-hero__tabs">{buttons}</div>'

    hidden = "" if is_active else " hidden"
    return f"""
<div class="lang-panel" data-lang="{lang_code}"{hidden}>
  <section class="rules-hero">
    <div class="container">
      <span class="eyebrow">{escape(l10n['kicker'])}</span>
      <h1 class="display">{escape(l10n['h1_pre'])} <em>{escape(l10n['h1_main'])}</em></h1>
      <p class="rules-hero__lede">{l10n['lede']}</p>
      {tabs_inline}
    </div>
  </section>

  <div class="page-body">
    <div class="container">
      <div class="rules-list">{rule_items}</div>
      <div class="rules-closing">
        <span class="rules-closing__mark">❦</span>
        <p>{escape(l10n['closing'])}</p>
      </div>
      <div class="emergency-card">
        <div class="emergency-card__icon">{ICON_PHONE}</div>
        <div class="emergency-card__body">
          <span class="emergency-card__eyebrow">{escape(l10n['emergency_eyebrow'])}</span>
          <h3>{escape(l10n['emergency_h3'])}</h3>
          <p>{escape(l10n['emergency_p'])}</p>
        </div>
        <div class="emergency-card__numbers">
          <a href="tel:02437471322" class="emergency-card__tel">024.3747.1322</a>
          <a href="tel:02432115793" class="emergency-card__tel">024.3211.5793</a>
        </div>
      </div>
    </div>
  </div>
</div>
"""


def render_noi_quy(art):
    """Nội quy tham quan — 3 self-contained panels (VI/EN/FR), tabs inside each hero."""
    raw_by_lang = {
        "vi": art.raw_text_vi or "",
        "en": getattr(art, "raw_text_en", "") or "",
        "fr": getattr(art, "raw_text_fr", "") or "",
    }
    langs = [code for code in ("vi", "en", "fr") if raw_by_lang[code].strip()]
    if not langs:
        langs = ["vi"]

    panels_html = "".join(
        _render_noi_quy_panel(code, raw_by_lang[code], is_active=(i == 0), all_langs=langs)
        for i, code in enumerate(langs)
    )

    tab_js = """
<script>
(function(){
  var tabs = document.querySelectorAll('.lang-tab');
  var panels = document.querySelectorAll('.lang-panel');
  if (!tabs.length || !panels.length) return;
  tabs.forEach(function(t){
    t.addEventListener('click', function(){
      var lang = t.dataset.lang;
      tabs.forEach(function(x){ x.classList.toggle('is-active', x.dataset.lang === lang); });
      panels.forEach(function(p){ p.hidden = p.dataset.lang !== lang; });
      if (window.matchMedia('(max-width: 768px)').matches) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });
})();
</script>
""" if len(langs) > 1 else ""

    return f"""
<div class="lang-panels">
{panels_html}
</div>
{tab_js}
"""


def build_tham_quan():
    """Rich visitor-focused /tham-quan/ landing + individual article pages."""
    src = ROOT / "Trang 2 Thăm quan"
    articles = []
    if src.exists():
        for f in sorted(src.iterdir()):
            if f.is_file() and f.suffix.lower() == ".docx":
                raw = vm.docx_to_text(f)
                langs = vm.split_languages(raw)
                title = vm.strip_lead_num(f.stem)
                imgs = vm.collect_images(f.parent)
                img_paths = [vm.copy_image(im, "tham-quan") for im in imgs]
                art = vm.Article(
                    slug=vm.slugify(title),
                    title_vi=title,
                    content_vi=vm.text_to_html(langs.get("vi", "")),
                    images=img_paths,
                    raw_text_vi=langs.get("vi", ""),
                    source_folder=f.parent,
                )
                if "en" in langs:
                    art.content_en = vm.text_to_html(langs["en"])
                    art.raw_text_en = langs["en"]
                if "fr" in langs:
                    art.content_fr = vm.text_to_html(langs["fr"])
                    art.raw_text_fr = langs["fr"]
                # Clean up Nội quy title & slug (source filename has "6-2" suffix)
                if "noi-quy" in art.slug or "nội quy" in art.title_vi.lower():
                    art.title_vi = "Nội quy tham quan"
                    art.slug = "noi-quy-tham-quan"
                articles.append(art)

    hero_img = _find_image("kvc", "gieng") or _find_image("kvc") or "/assets/images/hero.jpg"

    # Google Maps embed — Văn Miếu, 58 Quốc Tử Giám
    map_embed = (
        '<iframe '
        'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3724.'
        '1469437253!2d105.83282887503895!3d21.02897398062112!2m3!1f0!2f0!3f0'
        '!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3135ab94c4a6ce75%3A0xd4e3e29c6c'
        '37f0a3!2zVsSDbiBNaeG6v3UgUXX hu5FjIFThu60gR2nDoW0!5e0!3m2!1svi!2s!4v1" '
        'loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
        'allowfullscreen title="Bản đồ Văn Miếu – Quốc Tử Giám"></iframe>'
    )

    # Transport / parking data (real from Các tiện ích.docx)
    transports = [
        (ICON_CAR,   "Bãi đỗ ô tô",         "Phố Văn Miếu"),
        (ICON_BUS,   "Bãi đỗ xe máy · xe đạp", "Tại vườn Giám"),
        (ICON_TAXI,  "Taxi · Grab",          "Đón trả tại 58 Quốc Tử Giám"),
        (ICON_PIN,   "Đi bộ · xe buýt",      "Xem tuyến trên Google Maps"),
    ]
    transport_html = "".join(f"""
<div class="transport-card">
  <div class="transport-card__icon">{icon}</div>
  <h4>{title}</h4>
  <p>{desc}</p>
</div>""" for icon, title, desc in transports)

    # Amenities (real from Các tiện ích.docx + Dịch vụ tham quan.docx)
    amenities = [
        (ICON_USER_GUIDE, "Thuyết minh viên",    "VI · EN · CN · FR"),
        (ICON_HEADPHONE,  "Thuyết minh tự động", "8 ngôn ngữ"),
        (ICON_COFFEE,     "Café",                "Trong khuôn viên"),
        (ICON_GIFT,       "Đồ lưu niệm",         "Quà tặng văn hoá"),
        (ICON_BENCH,      "Hàng ăn",             "Tại khuôn viên"),
        (ICON_CAR,        "Bãi đỗ ô tô",         "Phố Văn Miếu"),
        (ICON_MAP_ICON,   "Bãi xe máy · xe đạp", "Vườn Giám"),
        (ICON_PHONE,      "Đặt dịch vụ",         "024.3823.5601"),
    ]
    amenity_html = "".join(f"""
<div class="amenity">
  <div class="amenity__icon">{icon}</div>
  <h4>{title}</h4>
  <p>{desc}</p>
</div>""" for icon, title, desc in amenities)

    # (Sections "Khám phá cùng chuyên gia" and "Tài liệu chi tiết" removed
    # per user request — all content now lives on the tham-quan hub itself.)

    # -------- Assemble page --------
    body = f"""
<section class="visit-hero">
  <div class="hero__media" role="img" aria-label="Văn Miếu – Quốc Tử Giám"
       style="position:absolute;inset:0;z-index:0;background:
         linear-gradient(180deg, rgba(28,25,23,.3) 0%, rgba(28,25,23,.6) 80%, rgba(28,25,23,.78) 100%),
         url('{hero_img}') center/cover no-repeat;">
  </div>
  <div class="container visit-hero__content">
    <div class="visit-hero__kicker">Tham quan</div>
    <h1>Lên kế hoạch cho <em>chuyến thăm</em></h1>
    <p class="visit-hero__lede">Mọi thông tin du khách cần — giờ mở cửa, giá vé, đường đi, tiện nghi và các chương trình tham quan có hướng dẫn.</p>
  </div>
</section>

<div class="page-body">
  <div class="container">

    <!-- GIỜ & VÉ -->
    <div style="margin-bottom:12px;">
      <span class="eyebrow">Giờ mở cửa &amp; vé</span>
      <h2 class="section-title" style="margin:10px 0 24px;">Thông tin tham quan</h2>
    </div>

    <div class="visit-info">
      <div class="info-card">
        <span class="info-card__eyebrow">Giờ mở cửa</span>
        <h3>Lịch mở cửa theo mùa</h3>
        <table class="hours-table">
          <tbody>
            <tr class="is-highlight"><td>Mùa hè (tháng 4 – 10)</td><td>07:30 – 18:00</td></tr>
            <tr><td>Mùa đông (tháng 11 – 3)</td><td>08:00 – 17:00</td></tr>
            <tr><td style="padding-top:18px;color:var(--ink-mute);font-weight:400;font-size:13px;">Ngày lễ · Tết</td><td style="padding-top:18px;color:var(--ink-mute);font-weight:400;font-size:13px;">Xác nhận qua hotline</td></tr>
          </tbody>
        </table>
        <p style="margin:18px 0 0;font-size:13px;color:var(--ink-mute);line-height:1.5;">
          Hotline xác nhận: <strong style="color:var(--brick);">024.3747.1322</strong> ·
          <strong style="color:var(--brick);">024.3211.5793</strong>
        </p>
      </div>

      <div class="info-card">
        <span class="info-card__eyebrow">Giá vé (theo Vé.docx)</span>
        <h3>Bảng giá tham quan</h3>
        <table class="price-table">
          <tbody>
            <tr class="is-featured">
              <td><div class="price-row__title">Người lớn</div><div class="price-row__sub">Vé tham quan tiêu chuẩn</div></td>
              <td>30.000đ</td>
            </tr>
            <tr>
              <td><div class="price-row__title">Học sinh · Sinh viên</div><div class="price-row__sub">Xuất trình thẻ học sinh/sinh viên</div></td>
              <td>15.000đ</td>
            </tr>
            <tr>
              <td><div class="price-row__title">Người lớn trên 60 tuổi</div><div class="price-row__sub">Xuất trình CMND / hộ chiếu</div></td>
              <td>15.000đ</td>
            </tr>
            <tr class="is-free">
              <td><div class="price-row__title">Trẻ em dưới 15 tuổi</div><div class="price-row__sub">Không cần vé · miễn phí hoàn toàn</div></td>
              <td>Miễn phí</td>
            </tr>
          </tbody>
        </table>
        <a href="/tham-quan/ve/" class="info-card__cta">Xem chi tiết vé {ICON_ARROW}</a>
      </div>
    </div>

    <!-- HƯỚNG DẪN ĐI LẠI -->
    <div style="margin-top:72px;">
      <span class="eyebrow">Đường đến &amp; Bãi đỗ xe</span>
      <h2 class="section-title" style="margin:10px 0 24px;">Cách đến Văn Miếu</h2>
    </div>

    <div class="directions-map">
      <a href="https://maps.app.goo.gl/VJuZqgHFvXgSHi8B7" target="_blank" rel="noopener" class="directions-map__cta">
        {ICON_EXTERNAL} Mở Google Maps
      </a>
      {map_embed}
    </div>

    <div class="transport-grid">{transport_html}</div>

    <!-- TIỆN NGHI -->
    <div style="margin-top:72px;">
      <span class="eyebrow">Dịch vụ &amp; Tiện ích</span>
      <h2 class="section-title" style="margin:10px 0 24px;">Tiện nghi tại khuôn viên</h2>
    </div>

    <div class="amenities-grid">{amenity_html}</div>

    <div class="a11y-banner">
      <div class="a11y-banner__icon">{ICON_A11Y}</div>
      <div>
        <h4>Hỗ trợ khách có nhu cầu đặc biệt</h4>
        <p>Vui lòng liên hệ trước qua hotline <strong>024.3747.1322</strong> hoặc <strong>024.3211.5793</strong> để được bố trí hỗ trợ phù hợp khi tham quan.</p>
      </div>
    </div>

    <!-- DỊCH VỤ THAM QUAN (từ dịch vụ tham quan.docx) -->
    <div class="booking-section" id="dat-dich-vu" style="margin-top:64px;">
      <span class="eyebrow">Dịch vụ tham quan</span>
      <h2 class="section-title" style="margin:10px 0 4px;">Bốn dịch vụ hỗ trợ du khách</h2>
      <p style="color:var(--ink-soft);max-width:620px;margin:0 0 24px;font-size:15px;">
        Liên hệ trực tiếp qua số điện thoại hoặc cán bộ tại Quầy bán vé để đặt các dịch vụ sau.
      </p>
      <div class="services-list">

        <div class="service-row">
          <div class="service-row__icon">{ICON_USER_GUIDE}</div>
          <div class="service-row__body">
            <h3>Thuyết minh viên trực tiếp</h3>
            <p>Bốn ngôn ngữ: Việt · Anh · Trung · Pháp — liên hệ trước hoặc hỏi cán bộ tại Quầy bán vé.</p>
          </div>
          <a href="tel:02438235601" class="service-row__cta">
            <span class="service-row__label">Điện thoại đặt trước</span>
            <span class="service-row__tel">024.3823.5601</span>
          </a>
        </div>

        <div class="service-row">
          <div class="service-row__icon">{ICON_HEADPHONE}</div>
          <div class="service-row__body">
            <h3>Thuyết minh tự động (audio guide)</h3>
            <p>8 ngôn ngữ: VI · EN · FR · ES · KO · JA · ZH · TH. Phí: Tiếng Việt 30.000đ · tiếng nước ngoài 50.000đ.</p>
          </div>
          <div class="service-row__cta service-row__cta--info">
            <span class="service-row__label">Nhận thiết bị tại</span>
            <span class="service-row__tel">Quầy bán vé</span>
          </div>
        </div>

        <div class="service-row">
          <div class="service-row__icon">{ICON_BOOK}</div>
          <div class="service-row__body">
            <h3>Chương trình khuyến học</h3>
            <p>Tổ chức cho trường học, đoàn học sinh — có chương trình riêng theo lứa tuổi.</p>
          </div>
          <a href="tel:0369087468" class="service-row__cta">
            <span class="service-row__label">Điện thoại đặt dịch vụ</span>
            <span class="service-row__tel">036.908.7468</span>
          </a>
        </div>

        <div class="service-row">
          <div class="service-row__icon">{ICON_STAR}</div>
          <div class="service-row__body">
            <h3>Tổ chức sự kiện</h3>
            <p>Sự kiện văn hoá, hội thảo, workshop tại khuôn viên di tích — liên hệ hotline chung.</p>
          </div>
          <a href="tel:02437471322" class="service-row__cta">
            <span class="service-row__label">Hotline liên hệ</span>
            <span class="service-row__tel">024.3747.1322</span>
          </a>
        </div>

      </div>
    </div>

    <!-- HIGHLIGHT NỘI QUY (replaces docs list) -->
    <a class="rules-highlight" href="/tham-quan/noi-quy-tham-quan/">
      <div class="rules-highlight__icon">{ICON_SHIELD}</div>
      <div class="rules-highlight__body">
        <span class="rules-highlight__eyebrow">Lưu ý quan trọng</span>
        <h3>Vui lòng đọc nội quy trước khi tham quan</h3>
        <p>8 điều Quý khách cần thực hiện để chuyến tham quan trọn vẹn và di tích được gìn giữ cho mai sau.</p>
      </div>
      <span class="rules-highlight__cta">
        Đọc nội quy tại đây
        {ICON_ARROW}
      </span>
    </a>

  </div>
</div>
"""
    vm.write_page(
        vm.SITE / "tham-quan" / "index.html",
        page("Tham quan", body, "/tham-quan/",
             [("/", "Trang chủ"), (None, "Tham quan")])
    )

    # Still generate individual article pages for each docx.
    # Nội quy gets a creative layout (8-card grid + hotline + lang tabs).
    for art in articles:
        bc = [("/", "Trang chủ"), ("/tham-quan/", "Tham quan"), (None, art.title_vi)]
        if "noi-quy" in art.slug or "nội quy" in art.title_vi.lower():
            page_body = render_noi_quy(art)
        else:
            page_body = render_article(art, bc)
        vm.write_page(
            vm.SITE / "tham-quan" / art.slug / "index.html",
            page(art.title_vi, page_body, "/tham-quan/", bc)
        )


# =========================================================================
# Sitemap wrapper (keep existing logic, just re-rendered through new page())
# =========================================================================
def build_site_map():
    pages = vm._collect_sitemap_pages()
    root = vm._build_sitemap_tree(pages)
    total = len(pages)
    top_nodes = vm._sort_sm_children(root["children"], is_root=True)
    tree_html = "".join(vm._render_sm_node(n) for n in top_nodes)

    body = f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Điều hướng</span>
    <h1>Sơ đồ trang</h1>
    <p class="lede">Toàn bộ {total} trang của website được sắp xếp theo cấu trúc phân cấp. Nhấn mũi tên để mở rộng, gõ vào ô tìm kiếm để lọc.</p>
  </div>
</section>
<div class="page-body">
  <div class="container">
    <div class="sm-toolbar">
      <input type="search" id="sm-search" class="sm-search" placeholder="Tìm trong sơ đồ… (phím tắt: / )" autocomplete="off" aria-label="Tìm trong sơ đồ trang">
      <button class="sm-btn" id="sm-expand" type="button">Mở rộng tất cả</button>
      <button class="sm-btn" id="sm-collapse" type="button">Thu gọn</button>
    </div>
    <p class="sm-stats" id="sm-stats"></p>
    <ul class="sm-tree">
    {tree_html}
    </ul>
    <script>{vm.SITEMAP_JS}</script>
  </div>
</div>
"""
    vm.write_page(
        vm.SITE / "so-do-trang" / "index.html",
        page(
            "Sơ đồ trang",
            body,
            "/so-do-trang/",
            breadcrumbs=[("/", "Trang chủ"), (None, "Sơ đồ trang")],
        ),
    )
    print(f"  → {total} trang trong sơ đồ.")


# =========================================================================
# Bind overrides & run
# =========================================================================
vm.CSS = NEW_CSS
vm.NAV_ITEMS = NAV_ITEMS
vm.page = page
vm.render_article = render_article
vm.render_listing = render_listing
vm.render_section_index = render_section_index
vm.render_program = render_program
vm.build_home = build_home
vm.build_tham_quan = build_tham_quan
vm.build_site_map = build_site_map


# Hand-written pages that live inside directories vm.main() wipes
# (di-tich/, tham-quan/, hoat-dong/, giao-duc-di-san/, ve-chung-toi/,
# so-do-trang/). They are backed up before the build and restored
# afterwards so repeated builds do not delete them.
PRESERVE_PATHS = [
    "di-tich/lich-su/dong-chay",
]


def _preserve_and_build():
    import shutil
    backup_root = vm.SITE / ".preserve-backup"
    if backup_root.exists():
        shutil.rmtree(backup_root)

    saved = []
    for rel in PRESERVE_PATHS:
        src = vm.SITE / rel
        if src.exists():
            dst = backup_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)
            saved.append(rel)
            print(f"  Preserving {rel}")

    try:
        vm.main()
    finally:
        for rel in saved:
            src = backup_root / rel
            dst = vm.SITE / rel
            if dst.exists():
                shutil.rmtree(dst)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)
            print(f"  Restored {rel}")
        if backup_root.exists():
            shutil.rmtree(backup_root)


if __name__ == "__main__":
    # Ensure asset dirs exist (old main() doesn't create css/)
    (vm.ASSETS / "css").mkdir(parents=True, exist_ok=True)
    vm.IMG_DIR.mkdir(parents=True, exist_ok=True)
    _preserve_and_build()
