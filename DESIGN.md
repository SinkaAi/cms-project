# DKCGI Design Spec — Phase 1: Vision & Language

**Project:** DKCGI Website Redesign  
**Phase:** 1 — Define the Vision  
**Date:** 2026-03-21  
**Status:** Draft (pending Denis approval)

---

## 🎯 Design Direction

**Reference:** Raycast (raycast.com) — Warm dark mode, editorial minimalism

**Philosophy:** The site should feel like a premium creative professional's portfolio — not a tech demo, not a gaming HUD. Warm, inviting, confident. The kind of site that makes you trust the person selling the product.

---

## 🌙 DARK MODE — "The Night Studio"

A warm, rich dark that invites you to stay. Think: a well-designed workspace at night.

### Color Palette

| Role | Variable | Hex | Notes |
|------|----------|-----|-------|
| Base Background | `--bg-base` | `#0C0C0C` | Deep warm charcoal — NOT pure black |
| Surface | `--bg-surface` | `#151515` | Cards, panels — creates elevation |
| Elevated | `--bg-elevated` | `#1C1C1C` | Dropdowns, tooltips |
| Input | `--bg-input` | `#1A1A1A` | Form fields |
| Border Default | `--border` | `#222222` | Subtle definition |
| Border Hover | `--border-hover` | `#333333` | Interactive focus |
| Text Primary | `--text-primary` | `#FFFFFF` | Headings, important content |
| Text Secondary | `--text-secondary` | `#999999` | Body text, descriptions |
| Text Muted | `--text-muted` | `#666666` | Captions, metadata, dates |
| **Accent** | `--accent` | `#FF6363` | **Warm coral — CTAs, links, highlights** |
| Accent Hover | `--accent-hover` | `#FF8080` | Lighter coral for hover states |
| Accent Muted | `--accent-muted` | `#2D1F1F` | Coral tint for backgrounds |
| Success | `--success` | `#4ADE80` | Green — positive states |
| Warning | `--warning` | `#FFB000` | Amber — caution states |
| Error | `--error` | `#F87171` | Red — error states |

### Typography

- **Primary Font:** `Inter` (Google Fonts)
  - Weights: 400 (body), 500 (medium emphasis), 600 (subheadings), 700 (headings)
  - Body line-height: `1.6`
  - Heading letter-spacing: `-0.02em`
- **Monospace:** `JetBrains Mono` (for code blocks)
- **Fallback stack:** `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

### Font Scale

```
--text-xs:   0.75rem   /* 12px — captions */
--text-sm:   0.875rem   /* 14px — metadata */
--text-base: 1rem       /* 16px — body */
--text-lg:   1.125rem   /* 18px — large body */
--text-xl:   1.25rem    /* 20px — small headings */
--text-2xl:  1.5rem     /* 24px — section headings */
--text-3xl:  1.875rem   /* 30px — page headings */
--text-4xl:  2.25rem    /* 36px — hero headings */
--text-5xl:  3rem       /* 48px — large hero */
```

### Spacing System (4px/8px Grid)

```
--space-1:  4px
--space-2:  8px
--space-3:  12px
--space-4:  16px
--space-6:  24px
--space-8:  32px
--space-10: 40px
--space-12: 48px
--space-16: 64px
--space-20: 80px
--space-24: 96px
```

### Radius

```
--radius-sm:  8px
--radius-md:  12px
--radius-lg:  16px
--radius-xl:  24px
--radius-full: 9999px
```

### Elevation (No Shadows — Color Layering Only)

| Level | Background | Use |
|-------|-----------|-----|
| Base | `#0C0C0C` | Page background |
| Surface | `#151515` | Cards, panels |
| Elevated | `#1C1C1C` | Dropdowns, tooltips |
| Overlay | `#222222` | Modals, popovers |

**Borders define space:** `1px solid #222222` (default) → `1px solid #333333` (hover/focus)

### Motion

- Transitions: `200ms ease` (fast, responsive)
- Hover lifts: subtle `translateY(-2px)` on cards
- No bouncing, no elastic, no exaggerated motion
- Background: **STATIC** — no animated grid, no particles, no scanlines

---

## ☀️ LIGHT MODE — "The Editorial"

Warm, clean, inviting. Think: premium print magazine digitized. A space that feels trustworthy for learning.

### Color Palette

| Role | Variable | Hex | Notes |
|------|----------|-----|-------|
| Base Background | `--bg-base-light` | `#FAFAF8` | Warm off-white — NOT pure white |
| Surface | `--bg-surface-light` | `#FFFFFF` | Cards, panels |
| Elevated | `--bg-elevated-light` | `#F5F5F3` | Dropdowns |
| Input | `--bg-input-light` | `#FAFAF8` | Form fields |
| Border Default | `--border-light` | `#E8E8E6` | Warm gray border |
| Border Hover | `--border-hover-light` | `#D0D0CC` | Darker warm gray |
| Text Primary | `--text-primary-light` | `#1A1A1A` | Near-black for warmth |
| Text Secondary | `--text-secondary-light` | `#666666` | Body text |
| Text Muted | `--text-muted-light` | `#999999` | Captions, metadata |
| **Accent** | `--accent-light` | `#E54545` | Slightly deeper coral for contrast |
| Accent Hover | `--accent-hover-light` | `#D13636` | Darker coral hover |
| Accent Muted | `--accent-muted-light` | `#FDF0F0` | Light coral tint |

### Typography

Same as dark mode: **Inter** for all text. Clean, modern, readable.

### Differences from Dark Mode

- Light mode uses **subtle shadows** instead of color layering (shadows feel natural in light contexts)
- `border-radius` stays the same (12px–16px)
- Generous whitespace is even more important in light mode

### Light Mode — What We REMOVE

- ❌ Animated mesh gradients (Apple clone — dated 2019-2020)
- ❌ Floating orbs
- ❌ Any animated background effects

### Light Mode — What We KEEP

- ✅ Warm off-white base
- ✅ Clean card surfaces with subtle shadows
- ✅ Same coral accent color (adjusted for contrast)
- ✅ Same typography system
- ✅ Same spacing and radius

---

## 🚫 WHAT WE'RE REMOVING (Alex's Audit Findings)

These elements from the current site feel dated/gimmicky and will be removed:

1. **Animated grid background** — Matrix screensaver effect, completely off for a CGI portfolio
2. **Floating particle system** — 20 radial gradients creating a cyberpunk screensaver vibe
3. **Scanline overlay** — CRT effect from the 90s, creates visual noise
4. **Animated logo** — Three spinning rings + glowing gradient text (gaming forum aesthetic)
5. **Glowing neon underlines on nav** — `box-shadow` neon glow = Web 2.0 circa 2008
6. **Orbitron + Rajdhani + Exo 2** — Three sci-fi fonts stacked inconsistently
7. **Glassmorphism on every element** — When everything is glass, nothing is glass
8. **Emoji as icons** — 🎓📺👨🎓⭐ in a professional portfolio feels juvenile
9. **Pulsing animations on cards** — Gaming HUD overlay aesthetic

---

## ✅ WHAT WE'RE KEEPING

1. **Dark/light theme toggle** — Already clean, localStorage persistence works well
2. **CSS custom properties** — Very well organized, keeps theme switching clean
3. **Responsive breakpoints** — Good grid behavior at 768px, 900px, 600px
4. **Post card layout** — Thumbnails, excerpts, category badges, dates — clean
5. **Blog toolbar** — Search + categories on same line
6. **Blog sidebar widgets** — Newsletter, recent posts, categories — solid
7. **Stats section** — Simple, honest, readable numbers
8. **Footer** — Simple and clean
9. **Content hierarchy** — H1/H2/H3 distinctions are clear
10. **Card hover lift effect** — Nice subtle interaction

---

## 📐 LAYOUT SYSTEM

### Container

```css
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 var(--space-6);     /* 24px mobile */
}

@media (min-width: 768px) {
  .container {
    padding: 0 var(--space-12);  /* 48px desktop */
  }
}
```

### Grid

```css
.grid {
  display: grid;
  gap: var(--space-6);
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 900px) {
  .grid-3, .grid-4 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
}
```

---

## 🔧 IMPLEMENTATION ORDER (Phase 2)

1. Replace CSS custom properties with new palette
2. Strip animated backgrounds (grid, particles, scanlines)
3. Replace fonts (import Inter + JetBrains Mono)
4. Build dark mode surface system
5. Build light mode surface system
6. Update buttons with new accent color
7. Update cards with new surface system
8. Update nav with refined hover states (no glow)
9. Simplify logo — static gradient or simple text
10. Test theme toggle — smooth transition

---

## 📸 REFERENCE SITES

| Site | URL | What to Study |
|------|-----|---------------|
| Raycast | raycast.com | Warm charcoal base, coral accent, Inter typography, layered surfaces |
| Mobbin | mobbin.com | Warm dark tones, clean card system, generous whitespace |
| Seek | seek.coffee | Similar dark palette, bento-grid layout |
| Linear | linear.app | Contrast with cold dark mode — shows why warm works |

---

## 👀 VISUAL CHECKPOINTS

After each step, we verify:

- [ ] Dark mode background feels warm, not cold
- [ ] Coral accent draws the eye without overwhelming
- [ ] Text is readable without eye strain
- [ ] Cards feel elevated through color, not shadow (dark mode)
- [ ] Cards feel grounded through subtle shadow (light mode)
- [ ] Theme toggle transitions smoothly
- [ ] No jarring visual effects or animations
- [ ] Typography hierarchy is clear at a glance

---

**Next step: Phase 2 — Build the Theme Engine**  
等着 Denis to approve this direction before moving forward.
