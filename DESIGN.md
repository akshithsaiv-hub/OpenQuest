# 🎨 Design Specification: Kisan Setu Design System

## 1. Design Philosophy & Tone
- **Tone:** Grounded, trustworthy, deeply respectful of rural livelihoods, and radically transparent.
- **Anti-Pattern Guardrails (No AI Slop):**
  - ❌ **No generic purple-to-blue AI gradients** or abstract futuristic neon glowing effects.
  - ❌ **No microscopic low-contrast text** (e.g., #999 on white).
  - ❌ **No nested card labyrinths** or confusing multi-click accordions for core benefits.
  - ✅ **Warm agricultural palette:** Lush field green, golden harvest amber, crisp clean surfaces, and distinct sovereign badges.
  - ✅ **Radical scannability:** A farmer in direct sunlight must clearly read the benefit amount in under 2 seconds.

---

## 2. Color System & Design Tokens

```css
:root {
  /* Brand Primaries */
  --color-primary: #1b5e20;        /* Deep Forest Green - Trust & Nature */
  --color-primary-light: #2e7d32;  /* Fresh Growth Emerald */
  --color-primary-dark: #0e3d13;   /* High Contrast Text Green */

  /* Harvest & Alerts */
  --color-harvest-gold: #f57f17;   /* Harvest Grain Gold */
  --color-alert-bg: #fff3e0;       /* Warning Alert Tint */
  --color-alert-border: #ffcc80;   /* Warning Border */
  --color-alert-text: #c43e00;     /* Emergency 72-hr Window Accent */

  /* Sovereign Government Attribution Badges */
  --badge-central-bg: #e8eaf6;     /* Saffron/Navy Central Scheme Tint */
  --badge-central-text: #1a237e;   /* Deep Sovereign Navy */
  --badge-central-border: #9fa8da;

  --badge-state-bg: #e8f5e9;       /* State Agriculture Tint */
  --badge-state-text: #1b5e20;     /* State Green */
  --badge-state-border: #a5d6a7;

  /* Neutrals & Surfaces */
  --surface-canvas: #f4f8f4;       /* Morning Field Canvas */
  --surface-card: #ffffff;         /* Pure Card White */
  --text-primary: #1f2937;         /* High-Contrast Charcoal (> 7:1) */
  --text-secondary: #4b5563;       /* Accessible Slate (> 4.5:1) */
  --border-subtle: #e5e7eb;
}
```

---

## 3. Typography & Accessibility Standards

### Type Hierarchy
- **Brand / Header 1:** 28px – 34px, 800 Extra-Bold, tight letter spacing.
- **Card Scheme Titles:** 20px – 22px, 800 Bold, line-height 1.35.
- **Benefit Numbers:** 18px – 20px, 800 Bold, Forest Green `#2e7d32`.
- **Body / Descriptions:** 16px, 400 Regular, line-height 1.6 (Strict minimum: never below 14px anywhere).
- **Badges & Labels:** 12px – 13px, 800 Bold, uppercase tracking.

### Touch & Accessibility Standards (WCAG 2.1 AA Compliant)
- **Minimum Touch Target:** All buttons, dropdowns, and interactive tabs have a minimum hit area of **48px × 48px** for easy single-thumb tapping on mobile.
- **Color Contrast:** All body text exceeds **4.5:1** contrast; all interactive headers exceed **7:1**.
- **Sunlight Readability:** High-contrast text on off-white cards ensures legibility under direct outdoor daylight.
- **Screen Reader Support:** Full ARIA role attribution (`role="banner"`, `role="tablist"`, `aria-selected`, `aria-live="polite"`).

---

## 4. Component Patterns

### A. State Picker Card
- Centered, high-elevation card with an unmistakable location icon (`🗺️`).
- Clear directive label: *"Select Your State / Union Territory"*.
- Smooth trigger that reveals schemes with instant smooth scrolling upon selection.

### B. The Scheme Card Architecture
Every scheme card follows a predictable, scannable layout:
1. **Top Badge Bar:** Central vs. State badge + Scheme Category tag.
2. **Title:** Large, localized scheme name.
3. **Description:** Plain-language summary (1–2 sentences).
4. **Benefit Banner:** Yellow/Gold highlight box featuring the exact financial amount or subsidy percentage.
5. **Eligibility Box:** Plain bullet points outlining land caps, age, and tenant eligibility.
6. **Document Checklist:** Green checkmark list of documents required.
7. **Emergency Window:** Red/Amber alert highlighting critical emergency claim windows (e.g., 72 hours for crop damage).
8. **Action Footer:** Official government portal link button (`↗`) with Last Verified timestamp.

### C. Persistent Language Selector
- Situated in the sticky top header at all times.
- Does not refresh or lose scroll position when toggled.
- Translates content client-side with zero network latency.
