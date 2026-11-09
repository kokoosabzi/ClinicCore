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


## Responsive shell contract

- Desktop: keep the application's existing right-to-left navigation rail, top header, content region, and workspace tab strip. Do not duplicate or replace permission-aware navigation.
- Narrow screens (900px and below): expose navigation through a compact menu control. The menu must remain scrollable, fit within the viewport, and close after navigation or with Escape. Store additionally uses a backdrop; Sabt and ClinicCore close on outside interaction.
- Keyboard: controls expose accessible names and expanded state; opening the menu moves focus into it, and Escape returns focus to the menu trigger.
- Workspace tabs: keep the strip horizontally scrollable and preserve the existing maximum-tab and session-restoration behavior.
- Theme: persist visual preferences locally; theme changes must update shared surfaces, controls, tables, navigation, and card contrast without changing application data.
- Print: hide floating theme controls, navigation drawers, and workspace tabs; preserve each application's own print/report layout.

## Current rollout status

- Foundation and theme engine: implemented in all three repositories.
- Responsive navigation behavior: integrated into each existing application shell.
- Workspace tabs: integrated with each repository's existing navigation model.
- Page-level redesign: not yet complete; forms, tables, dashboards, and reports remain application-specific and should be migrated in reviewed groups.
- Visual QA: automated Chromium coverage is in place for theme persistence, navigation behavior, workspace tabs, and narrow viewports. A final human review on the target Windows desktop and mobile devices remains recommended.

## Project-specific adaptations
- Sabt: contract workflow, transfers, bulk import, and Jalali reporting.
- ClinicCore: patients, appointments, clinical workflows, and clinic schedule.
- Store: sales, purchases, inventory, people, accounts, and reports.
