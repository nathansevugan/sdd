# Design System

## Design Tokens

```scss
// Colors
$color-primary:     #0F62FE;
$color-primary-dark:#0043CE;
$color-surface:     #FFFFFF;
$color-bg:          #F4F4F4;
$color-text:        #161616;
$color-text-muted:  #6F6F6F;
$color-border:      #E0E0E0;
$color-danger:      #DA1E28;
$color-success:     #198038;
$color-warning:     #F1C21B;

// Spacing (8pt grid)
$space-xs:   4px;
$space-sm:   8px;
$space-md:   16px;
$space-lg:   24px;
$space-xl:   40px;
$space-2xl:  64px;

// Typography
$font-display: 'IBM Plex Sans', sans-serif;
$font-mono:    'IBM Plex Mono', monospace;
$font-size-base: 14px;
$line-height:    1.5;

// Elevation
$shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
$shadow-md: 0 4px 12px rgba(0,0,0,0.15);
$shadow-lg: 0 8px 32px rgba(0,0,0,0.20);

// Motion
$ease-standard: cubic-bezier(0.2, 0, 0.38, 0.9);
$duration-fast:   100ms;
$duration-base:   200ms;
$duration-slow:   400ms;

// Radius
$radius-sm: 2px;
$radius-md: 4px;
$radius-lg: 8px;
```

## Typography Scale

| Token       | Size  | Weight | Usage          |
|-------------|-------|--------|----------------|
| `display-1` | 54px  | 300    | Hero headings  |
| `heading-1` | 32px  | 400    | Page titles    |
| `heading-2` | 24px  | 600    | Section titles |
| `body-long`  | 16px  | 400    | Body copy      |
| `body-short` | 14px  | 400    | UI labels      |
| `code`       | 13px  | 400    | Code blocks    |
| `caption`    | 12px  | 400    | Helpers/hints  |

## Iconography

- Library: **Material Symbols** (outlined, weight 300)
- Size grid: 16 / 20 / 24px only
- Never stretch or recolor icons outside the palette

## Imagery & Illustration

- Prefer geometric / abstract over photography
- SVG preferred; PNG only when SVG unavailable
- Always include `alt` text
