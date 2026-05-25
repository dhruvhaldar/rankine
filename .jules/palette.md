## 2024-06-25 - Fix ambiguous download link text and add visual polish
**Learning:** Combating WCAG Link Purpose violations for identical visual labels (e.g., "Download Plot") using explicit, context-specific `aria-label` tags paired with `aria-hidden="true"` emojis creates an accessible, visually polished pattern.
**Action:** Always combine context-specific `aria-label` properties with `aria-hidden="true"` decorative elements to provide visual delight while maintaining screen reader clarity.
## 2023-10-27 - Programmatic Focus and Generic Regions
**Learning:** In forms that reload the page and use hash links to shift focus to results, applying `tabindex="-1"` appropriately moves browser focus but results in an ugly default focus ring wrapping the entire content area on most browsers. Additionally, applying `aria-label` to generic `<div>` tags is often ignored by screen readers.
**Action:** When creating focusable result containers, always apply `[tabindex="-1"]:focus { outline: none; }` to remove the default outline, and ensure the container has `role="region"` so that its `aria-label` is consistently announced when focus shifts.
## 2026-05-06 - Context-Specific ARIA Labels and Respecting Reduced Motion
**Learning:** When displaying dynamically generated result blocks to screen readers, using a generic `aria-label="Calculation Result"` across multiple forms causes ambiguity about which result is being presented. Additionally, when using CSS animations (like a fade-in) to smooth out server-rendered page load state changes, failing to respect `prefers-reduced-motion` can negatively affect users with vestibular disorders.
**Action:** Always provide context-specific `aria-label` attributes for dynamic results (e.g., `"Nozzle Flow Result"`) and wrap any state transition animations in a `@media (prefers-reduced-motion: reduce)` block to ensure they gracefully degrade to `animation: none` for users who require it.

## 2024-05-18 - Prevent iOS Safari Auto-Zoom on Inputs
**Learning:** By default, iOS Safari will aggressively auto-zoom the page when a user focuses on a text or number `<input>` field if its font size is smaller than 16px. This creates a jarring UX where users are forced to manually pinch-to-zoom out after typing, particularly on mobile calculation tools.
**Action:** Always ensure that `input[type="text"]` and `input[type="number"]` have a CSS `font-size: 16px;` rule (or larger) to prevent this automatic scaling while preserving the mobile layout.
## 2026-05-08 - Target Anchor Breathing Room
**Learning:** When form submissions reload the page and jump to a specific element using hash fragments (like `#result`), the targeted element usually snaps flush against the top of the viewport. This feels claustrophobic and can obscure context. Adding `scroll-margin-top` to `:target` provides essential breathing room, and pairing it with `scroll-behavior: smooth` adds a pleasant, subtle visual transition that makes the jump feel less abrupt. However, it is critical to always provide a fallback to `scroll-behavior: auto` in a `prefers-reduced-motion` media query to prevent motion sickness for sensitive users.
**Action:** Whenever using hash links for in-page navigation or form result display, implement `:target { scroll-margin-top: [size]; }` and apply smooth scrolling with an explicit reduced-motion fallback.
## 2024-05-18 - Accessible Keyboard Shortcuts with Graceful Degradation
**Learning:** Adding explicit keyboard shortcuts (like Ctrl+Enter) to forms significantly improves power-user UX. However, statically displaying these shortcuts in the UI can be confusing for mobile users who don't have physical keyboards. Furthermore, screen readers need dedicated ARIA attributes (like `aria-keyshortcuts`) rather than just raw visual text to properly announce these capabilities.
**Action:** When implementing form submission keyboard shortcuts, always combine `aria-keyshortcuts` on the button for screen readers with a visual `<kbd aria-hidden="true">` element. Critically, use a `@media (pointer: coarse)` CSS query to gracefully hide the visual `<kbd>` hint on touch-based devices where the shortcut is inapplicable.
## 2026-05-11 - Dynamic OS-Specific Keyboard Shortcut Hints
**Learning:** Hardcoding a Mac-specific shortcut hint like `⌘↵` (or a verbose `Ctrl+Enter / Cmd+Enter`) in forms with keyboard shortcuts can confuse non-Mac users or clutter the UI. Furthermore, static `aria-keyshortcuts` attributes are not optimal when the exact OS shortcut differs.
**Action:** Always dynamically detect the user's OS via `navigator.userAgent.includes('Mac')` on the client side to cleanly update `<kbd>` text, `title` attributes, and explicit `aria-keyshortcuts` attributes to match their specific operating system (`Meta+Enter` vs `Control+Enter`).
## 2026-05-12 - Separate Form Helper Text from Labels
**Learning:** Nesting verbose helper text or instructions (like `<small>`) inside a `<label>` element forces screen readers to read the entire monolithic block of text as the accessible name for the input. This is confusing and disrupts the user's ability to quickly identify the input.
**Action:** Always extract helper text out of the `<label>`, assign it a unique ID, and programmatically link it to the `<input>` using the `aria-describedby` attribute. This allows the screen reader to clearly announce the label first, followed by the description.
## 2024-05-13 - Prevent Browser Interference on Technical Text Inputs
**Learning:** Browsers natively apply spellcheck, autocapitalize, and autocorrect to `<input type="text">` fields. For technical strings like a comma-separated list of Mach numbers (e.g., "2.0, 3.0"), these corrections cause squiggly error lines and disruptive auto-corrections, harming the UX.
**Action:** When creating text inputs intended for technical data or formatting (like code or mathematical arrays), always explicitly add `spellcheck="false" autocorrect="off" autocapitalize="none"` to prevent unhelpful browser interference.

## 2024-05-13 - Improve Loading Button Semantics
**Learning:** While `cursor: not-allowed` is appropriate for a truly disabled button, a button temporarily deactivated during an async submission (often indicated by `aria-disabled="true"` and a loading spinner) should communicate that it is processing, not permanently blocked. Using `cursor: not-allowed` creates cognitive dissonance when the user is explicitly waiting for the result of their click.
**Action:** Split the CSS for disabled states. Use `cursor: not-allowed` for `button:disabled` (permanently unclickable), and `cursor: wait` for `button[aria-disabled="true"]` (temporarily processing).
## 2026-05-14 - Aligning Implicit Backend Bounds with Frontend HTML5 Validation
**Learning:** In forms relying heavily on numeric inputs, native HTML5 validation (like `min="0"`) allows inclusive values (e.g., `0`) by default. However, when the backend requires *strictly positive* bounds (e.g., `value > 0`), submitting `0` bypasses frontend checks and triggers a context-breaking raw 400 server error, which disrupts user workflow.
**Action:** Always align exclusive backend bounds with frontend HTML5 inline validation. For variables that must be strictly positive, combine `min="0"` with a JavaScript `input` event listener that sets native validation via `this.setCustomValidity('Value must be strictly positive (greater than 0).')` if the value is `<= 0`.
## 2026-05-15 - Quick Navigation as Dual-Purpose Table of Contents & Skip Links
**Learning:** For single-page applications with vertically stacked, complex calculation tools, users often have to scroll past forms they aren't interested in to reach their desired tool. Traditional hidden skip links (e.g., "Skip to Main Content") only benefit screen reader and keyboard users. By creating a visible, styled "Quick Navigation" block of jump links at the top of the page, we simultaneously provide a scannable table of contents for mouse users and highly visible, accessible skip links for keyboard users, drastically reducing friction for everyone.
**Action:** On pages with multiple stacked, distinct functional blocks or sections, implement a visible `<nav aria-label="Quick Navigation">` block with anchor links jumping directly to the section IDs. Ensure the target sections have `tabindex="-1"` and an appropriate `aria-labelledby` or `aria-label` to ensure focus moves correctly.
## 2024-05-18 - Preserve Calculator Input State
**Learning:** When building iterative calculation tools that reload the page on submission without server-side input re-population, aggressively clearing `sessionStorage` upon successful submission forces users to re-enter all data if they want to tweak a single parameter. This causes significant friction for exploration.
**Action:** For iterative tools and calculators, do NOT clear `sessionStorage` form state upon submission. Allow the stored state to persist so users can seamlessly tweak inputs and recalculate without starting over.

## 2024-05-18 - Preserve State Across Path Changes
**Learning:** When using `sessionStorage` to preserve form inputs, namespacing keys by `window.location.pathname` breaks state preservation for forms that change the URL path upon submission (e.g., from `/` to `/plot/nozzle`), causing inputs to reset and frustrating users who want to tweak parameters.
**Action:** For single-page tools where form submissions alter the URL path, use a static, app-wide `sessionStorage` prefix (e.g., `const storagePrefix = 'form_state_rankine_';`) instead of dynamically relying on `window.location.pathname`.
## 2024-05-21 - Fix stuck loading buttons on back navigation (BFCache)
**Learning:** When using JavaScript to change button states to "Calculating..." upon form submission, users navigating "back" via the browser's Back-Forward Cache (BFCache) will see a stuck loading button.
**Action:** Always listen for the `pageshow` event and check `event.persisted` to restore the button's original state and `aria-disabled` attributes if the page is restored from cache.

## 2024-05-22 - Dynamic Page Titles for Server-Rendered Form Results
**Learning:** When a form submission relies on a full server-side reload rather than AJAX, screen readers announce the page title again. If the title is static (e.g., just the app name), users lose context about whether their submission was successful or what state the page is in without navigating through the DOM.
**Action:** Always dynamically update the `<title>` tag for server-rendered result pages (e.g., prepending "Result - ") to immediately inform screen readers of the new state upon load.

## 2024-05-23 - Print Stylesheets for Engineering Tools
**Learning:** Users of scientific/engineering tools often print or save calculation results as PDFs for reporting. Without print stylesheets, the resulting PDF contains UI clutter like navigation links, buttons, and form helper text, making it look unprofessional.
**Action:** Always include a `@media print` block to hide interactive UI elements (`nav`, `button`, `.empty-state`, etc.), remove styling from input fields to display them as raw text, and use `page-break-inside: avoid` on sections and images to ensure cleanly formatted printed reports.

## 2026-05-24 - Descriptive Image Alt Text for Data Visualizations
**Learning:** Screen readers rely on the `alt` attribute of `<img>` tags to describe visual content. When rendering complex, dynamically generated data visualizations (like Matplotlib charts), using generic, unhelpful `alt` text (e.g., "Nozzle Plot" or "Shock Polar") provides no value and deprives visually impaired users of essential context.
**Action:** Always provide highly descriptive, context-specific `alt` text for generated charts and plots. Describe the type of chart, what the axes represent, and what relationship or trend is being visualized (e.g., "Line graph showing pressure and Mach number distribution through the converging-diverging nozzle").

## 2024-05-25 - Visually Indicating Stale Form Results
**Learning:** In calculator applications where results are displayed statically below the form, editing inputs without submitting immediately makes the visible result "stale" (no longer matching the inputs). Users can easily mistake the old graph for the new parameters. Dimming the result and adding an explicit aria-label/title indicating it is stale provides essential visual and screen reader feedback that a recalculation is necessary.
**Action:** For forms that generate static plots or complex results, add an `input` event listener that safely applies a stale visual state (`opacity`, `grayscale`) and updates accessibility attributes (`aria-label`, `title`) on the result container as soon as the user alters an input.
