# Koko UI System — Integration Notes

## Design direction
Adopt the supplied Persian RTL dashboard references: soft blue/lavender canvas, white elevated surfaces, pastel gradient action cards, compact KPI tiles, rounded controls, subtle shadows, and a right-side navigation model where supported by the existing application shell.

## Shared tokens
- Canvas: pale blue/lavender (#eef1ff)
- Surface: white
- Primary action: blue (#496cf0)
- Accent families: blue, mint, lilac, pink, peach, yellow
- Radius: 11px controls / 18px cards
- Typography: Vazirmatn with safe Persian fallbacks
- Direction: RTL
- Focus: visible keyboard focus ring
- Motion: subtle and disabled for reduced-motion users

## Implementation constraints
1. This layer is presentation-only; do not alter business rules, APIs, permissions, database schemas, or financial/workflow behavior.
2. Keep each repository's framework and component architecture intact.
3. Preserve print styles, responsive behavior, accessibility, and existing theme settings.
4. Apply gradients to action/KPI cards, not dense data tables or long-form content.
5. Right sidebar and tabbed workspace are the target shell pattern; migrate each application shell in a separate reviewed step.
6. Do not introduce remote runtime dependencies for fonts, icons, or CSS.

## Rollout
- Foundation: shared tokens and safe component overrides.
- Shell: right navigation, top header, tabs, user/status area.
- Pages: dashboard, operational shortcuts, forms, tables, reports.
- QA: desktop/tablet/mobile, RTL, keyboard, dark mode, print, and existing automated tests.

## Project-specific adaptations
- Sabt: contract workflow, transfers, bulk import, and Jalali reporting.
- ClinicCore: patients, appointments, clinical workflows, and clinic schedule.
- Store: sales, purchases, inventory, people, accounts, and reports.
