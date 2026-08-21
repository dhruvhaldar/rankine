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

## 2026-05-26 - High Contrast for Keyboard Shortcut Hints
**Learning:** Using a white semi-transparent overlay (`rgba(255, 255, 255, 0.2)`) for keyboard shortcut hints (`<kbd>`) placed inside a colored button (like a primary blue submit button) often fails WCAG text contrast requirements because the white text inside the `<kbd>` blends into the lightened background.
**Action:** When designing `<kbd>` elements to sit inside colored buttons, use a dark semi-transparent overlay (`rgba(0, 0, 0, 0.2)`) instead. This darkens the background behind the shortcut, ensuring the white text remains legible and achieves proper contrast.

## 2026-05-27 - Auto-format Technical String Inputs on Blur
**Learning:** Native HTML5 `pattern` validation on technical strings (like comma-separated lists) is extremely strict and unforgiving of minor formatting typos (like trailing commas or erratic spacing), blocking submission and frustrating users.
**Action:** Instead of just failing validation, attach a `blur` event listener to technical string inputs that automatically cleans up and normalizes the input formatting (e.g., stripping trailing commas, normalizing spaces) when the user clicks away, providing a magical, frictionless UX.

## 2024-06-01 - Context for External Links
**Learning:** Links that open in a new tab (`target="_blank"`) without explicit warning disrupt the browsing experience, especially for screen reader users whose back button workflow is broken without their knowledge.
**Action:** Always append a visual indicator (like an `↗` arrow with `aria-hidden="true"`) to external links, and provide an explicit `aria-label` (e.g., `aria-label="Link Name (opens in a new tab)"`) or a visually hidden span to warn screen reader users of the context shift before they click.

## 2026-05-29 - Explicit Visual Overlays for Stale States
**Learning:** Relying solely on dimming (`opacity`) or grayscale effects to indicate a stale state on data visualizations can be ambiguous for users, who might mistake the dimming for an error or a loading state.
**Action:** Always combine dimming with an explicit text overlay (e.g., using an `::after` pseudo-element with `content: "Stale - Please Recalculate"`) positioned absolutely over the result container to unambiguously communicate the state and required action to the user.

## 2026-06-01 - Improve Primary Action Color Contrast
**Learning:** Using overly bright accent colors (like `#0070f3`) for interactive elements (links, focus outlines, and buttons) often fails WCAG contrast requirements against standard light backgrounds (like white `#ffffff` or light gray `#f0f4f8`), making them difficult to read for visually impaired users and reducing overall legibility.
**Action:** When defining a primary brand or interactive color scheme, always select a sufficiently dark shade (e.g., `#005bb5`) that maintains a contrast ratio of at least 4.5:1 against the application's light background colors, ensuring all links, buttons, and focus indicators are highly visible.

## 2026-06-02 - WCAG 2.5.3 Label in Name for Voice Dictation
**Learning:** When adding descriptive `aria-label`s to buttons that already have visible text (e.g., adding context to a "Download" button), replacing the entire label with a new phrase (e.g., "Download Nozzle Flow Plot" when the visible text is "Download Plot") violates the WCAG 2.5.3 Label in Name criterion. This breaks voice dictation software, as the user will say "Click Download Plot," but the software cannot find an element with that exact string in its accessible name.
**Action:** Always ensure the exact visible text string of a control is included continuously within its `aria-label`. For context-specific buttons, append the context in parentheses after the visible text (e.g., `aria-label="Download Plot (Nozzle Flow)"`).

## 2026-06-06 - Dynamic aria-invalid for Form Fields
**Learning:** Native HTML5 validation uses the `:invalid` pseudo-class for styling, but screen readers don't always announce the invalid state automatically unless `aria-invalid="true"` is explicitly set on the element.
**Action:** Attach event listeners to form inputs to dynamically toggle `aria-invalid="true"` based on the element's validation state (`input.validity.valid`).

## 2026-06-11 - Accessible Placeholder Text Contrast
**Learning:** Default browser placeholder colors (often `#a9a9a9` or similar) frequently fail WCAG AA contrast requirements (4.5:1) against standard white backgrounds, rendering the hint text illegible for users with visual impairments. Furthermore, some browsers apply a default opacity (e.g., `0.54` in Chrome) which further reduces contrast.
**Action:** Always explicitly style `::placeholder` with a sufficient contrast color (e.g., `#6b7280`) and set `opacity: 1` to override browser defaults and ensure placeholder text is accessible.

## 2024-06-25 - Interactive Elements in Stale States
**Learning:** When applying a visual 'stale' state (e.g., dimming or grayscale) to a container after inputs change, visually dimming it is insufficient to prevent interaction.
**Action:** Always explicitly disable interactive children within the stale container (e.g., by applying `pointer-events: none`, `tabindex="-1"`, and `aria-disabled="true"` to links or buttons) to prevent users from accidentally interacting with or exporting out-of-sync artifacts.

## 2024-06-26 - Result-to-Form Navigation Loop
**Learning:** In single-page calculators or tools that render results at the bottom of a long form, users frequently need to iterate and tweak parameters. Forcing them to manually scroll back up past large visualization artifacts introduces friction, especially on mobile.
**Action:** Always provide a quick anchor link (e.g., "Edit Inputs") alongside the generated results that targets the form's section ID, creating a seamless, accessible navigation loop for iterative workflows.

## 2024-06-27 - Skip to Content Links
**Learning:** For users relying on keyboard navigation or screen readers, having to repeatedly tab through top-level navigation blocks (like the Quick Navigation links) on every page refresh or form submission adds severe friction to their workflow.
**Action:** Always include a "Skip to main content" link as the very first interactive element in the `<body>`. Visually hide it by default (e.g., placing it off-screen) but make it visible upon receiving keyboard focus (`:focus`) to seamlessly support keyboard accessibility without cluttering the visual UI.

## 2024-06-28 - Hide Spin Buttons on Scientific Numeric Inputs
**Learning:** For scientific and engineering applications, native HTML numeric input spin buttons (up/down arrows) are a visual anti-pattern. They clutter the UI on hover/focus and are practically useless for precise decimal data (e.g., 0.05) or large magnitudes (e.g., 101325), as incrementing by a static step size is rarely the intended interaction.
**Action:** Always use CSS (`-webkit-appearance: none;` and `-moz-appearance: textfield;`) to visually hide the spin buttons on `input[type="number"]` when designing technical calculation tools, providing a cleaner, text-like interface.

## 2026-06-27 - Focusable Skip Link Targets
**Learning:** When a 'Skip to main content' link points to a container (like `<main>`), the target container must be programmatically focusable. If it lacks `tabindex="-1"`, the browser won't move the focus there, causing subsequent tab actions to restart from the top of the page, completely defeating the skip link's purpose.
**Action:** Always add `tabindex="-1"` to the target element of a skip link to allow it to receive focus programmatically.

## 2024-06-29 - Target Pulse Highlight for In-Page Navigation
**Learning:** When using in-page anchor links (like a "Skip to Content" or "Quick Nav" sidebar), users can sometimes lose track of where they landed on the page, especially on long, text-heavy forms where the target section blends in. Just jumping to the section isn't always enough visual feedback.
**Action:** Add a subtle, temporary CSS animation (e.g., `@keyframes` pulsing the `background-color`) to the `:target` pseudo-class to draw the user's eye directly to the newly focused section. Always respect `@media (prefers-reduced-motion: reduce)` by disabling this animation for users with vestibular disorders.

## 2026-07-06 - Inline Form Validation
**Learning:** Relying solely on color changes (like a red border or background) to indicate form validation errors violates WCAG 1.4.1 (Use of Color). Screen readers and colorblind users may miss the error state entirely if there is no text indicating what went wrong.
**Action:** Always provide an explicit, non-color-dependent visual indicator, such as an inline text error message displaying the native HTML5 `validationMessage`, linked to the input via `aria-describedby` and dynamically updated on `input`/`blur` events.

## 2026-07-07 - Actionable Pattern Validation Errors
**Learning:** When using HTML5 `pattern` attributes for input validation, the default browser `validationMessage` on a `patternMismatch` is often a generic 'Please match the requested format.', which is unhelpful.
**Action:** Always check for `input.validity.patternMismatch` and dynamically replace the generic message with the explicit format instructions provided in the input's `title` attribute to provide actionable feedback to users.

## 2026-07-08 - Synchronous Event Processing for Custom Validity
**Learning:** When using HTML5 `setCustomValidity` in an `input` event listener, if a generic UI listener (like one that toggles `aria-invalid` or displays `validationMessage`) is attached *before* the custom validation listener, the UI will read the input's previous validity state. This causes error messages to visually lag one keystroke behind the actual data.
**Action:** Always register custom validation constraints *before* generic validation UI handlers in the DOM execution order. Additionally, when one field's state dynamically restricts another (e.g., `min`/`max`), explicitly dispatch a synthetic `input` event on the dependent field to immediately trigger re-evaluation of its validity state.

## 2026-07-11 - Explicit Synthetic Event Dispatch for sessionStorage Restores
**Learning:** Restoring form field values from `sessionStorage` programmatically on page load using `element.value = storedValue` does not natively trigger standard input/change events. Without explicit re-dispatching of these events, custom inline validation and accessible elements relying on input attributes like `aria-invalid` become visibly disconnected and outdated compared to the actual field content upon reload.
**Action:** When implementing front-end state persistence across navigations/reloads, always complement setting the field value with an explicit synthetic event dispatch (e.g., `element.dispatchEvent(new Event('input', { bubbles: true }));`) to explicitly resync dynamic UI validation and accessibility states natively to the users.
## 2024-05-18 - Stale State Overlay Contrast
**Learning:** When creating a 'stale' or 'processing' overlay using an `::after` pseudo-element on a container, applying `opacity` or `filter: grayscale()` directly to the parent container creates a stacking context where the overlay text inherits the reduced opacity. This washes out the text and often causes severe WCAG color contrast violations against the content behind it.
**Action:** Always apply visual dimming effects (like `opacity` or `grayscale`) to the specific child elements inside the container (e.g., the target image or data wrapper) rather than the parent container, ensuring the overlay text remains fully opaque and highly readable.

## 2026-07-14 - Native Invalid Event Binding for Form Submissions
**Learning:** When building custom inline form validation that binds to `input` and `blur` events, form submissions containing invalid (or empty required) fields that have not been interacted with bypass these events. The browser fires a native `invalid` event instead, leaving the custom inline UI completely out of sync with the actual validation state.
**Action:** Always explicitly bind custom validation UI update functions to the native `invalid` event (`input.addEventListener('invalid', ...)`) in addition to `input` and `blur` to guarantee the inline error messages consistently appear when users submit incomplete or invalid forms.

## 2026-07-15 - Prevent Active Animations on aria-disabled Elements
**Learning:** While native `disabled` attributes automatically suppress CSS `:active` states in most browsers, elements that rely on `aria-disabled="true"` for logical disablement (like "Calculating..." buttons) will still trigger `:active` pseudo-classes (e.g., scaling or pressing animations) when clicked. This gives users false feedback that the button is still interactive.
**Action:** Always explicitly nullify interactive animations (e.g., `transform: none !important;`) on `[aria-disabled="true"]` selectors to ensure the visual feedback correctly reflects the disabled state.

## 2026-07-15 - Distinguishable Invalid Focus States
**Learning:** When styling invalid form fields, forcing the `outline-color` to red to match the error border causes the focus ring to blend into the error state. This violates WCAG Focus Appearance guidelines because the focus indicator loses contrast against the component's own border, making it harder for users (especially those with color blindness) to identify which element has keyboard focus.
**Action:** Always maintain the standard, highly visible focus ring color (e.g., brand blue) on invalid inputs. Allow the background and border to communicate the error, while the distinct outline color clearly communicates focus.

## 2026-07-16 - Prevent Active Animations on aria-disabled Elements
**Learning:** While native `disabled` attributes automatically suppress CSS `:active` states, elements that rely on `aria-disabled="true"` for logical disablement will still trigger `:active` pseudo-classes (e.g., scaling or pressing animations) when interacted with, providing false visual feedback.
**Action:** Always explicitly nullify interactive animations (e.g., `transform: none !important;`) on `[aria-disabled="true"]` selectors to ensure the visual feedback correctly reflects the disabled state.
## 2026-07-20 - Smooth Validation Layout Shifts
**Learning:** Toggling `display: none` to `display: block` for inline error messages causes abrupt, jarring layout shifts that push content down violently. Furthermore, some older screen readers fail to consistently announce `aria-live` updates on elements that are abruptly injected into the render tree via `display` toggling.
**Action:** Always use CSS transitions (`max-height`, `opacity`, `margin`, `overflow: hidden`) instead of `display` toggling for dynamic inline elements to create smooth, delightful micro-interactions that preserve accessibility, ensuring to include a `prefers-reduced-motion: reduce` fallback.

## 2024-07-23 - Native Validation Tooltip Clash
**Learning:** When combining custom inline validation messages with HTML5 native constraints, the browser's native validation tooltips will still appear on submit, visually clashing and overlapping with the custom inline UI.
**Action:** Always intercept the native `invalid` event using a capture phase listener on the form to call `e.preventDefault()`, which suppresses the native tooltip. Ensure to manually implement smooth scrolling and focus management for the first invalid field, as preventing the default action also disables the browser's native auto-focus behavior.

## 2026-07-26 - Smooth Validation Layout Shifts Fix
**Learning:** Clearing the text content of an inline error message synchronously when the input becomes valid immediately drops its intrinsic height to 0, completely bypassing CSS transitions (like max-height and margin) meant to smoothly collapse it. This causes an abrupt layout shift.
**Action:** When an input becomes valid, wrap the removal of the error text content in a `setTimeout` matching the CSS transition duration (e.g., 300ms) so the element has time to animate closed before its text is removed.

## 2026-08-01 - Programmatic Scroll Reduced Motion
**Learning:** When triggering programmatic scrolls via JavaScript's `element.scrollIntoView({ behavior: 'smooth' })`, this explicitly overrides any CSS `scroll-behavior` rules, causing forced animations for users who have requested reduced motion at the OS level.
**Action:** Always dynamically check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before executing programmatic scroll animations and fall back to `behavior: 'auto'` if true.
## 2026-08-04 - Robust Focus Ring Styling
**Learning:** Setting `outline-color` in CSS (especially for `:focus-visible` pseudo-classes on invalid fields) is often insufficient because the browser's default `outline-style` or `outline-width` might be set to `none` or a very thin 1px line, causing the focus ring to fail to render properly or lack enough prominence.
**Action:** Always use the explicit `outline` shorthand property (e.g., `outline: 2px solid [color];`) when styling custom focus states to guarantee the focus indicator overrides browser defaults, is sufficiently thick, and consistently satisfies WCAG Focus Appearance guidelines.

## 2026-08-05 - Focus Ring Offset for Invalid States
**Learning:** When styling invalid form fields with a distinct focus ring color (e.g., blue) that differs from the error border color (e.g., red), omitting `outline-offset` causes the two colors to touch directly. This reduces the distinctiveness of the focus ring and can create muddy contrast where the colors meet.
**Action:** Always include `outline-offset: 2px` (or similar) on `:focus-visible:invalid` states to ensure a clear visual separation between the error border and the focus indicator.

## 2026-08-03 - Programmatic Focus on Page Load with Hash
**Learning:** When traditional form submissions reload the page and use a URL hash (e.g., `#result`) to visually scroll to the result, the keyboard focus remains at the top of the document. This forces keyboard and screen reader users to tab through the entire page again to reach the new content.
**Action:** Always check for `window.location.hash` on page load (e.g., inside `DOMContentLoaded`) and programmatically move focus to the target element using `target.focus({ preventScroll: true })`. Ensure the target container has `tabindex="-1"`.

## 2026-08-05 - Stale State Accessibility Announcement
**Learning:** When dynamically changing decoupled visual states (like making a result container 'stale' when inputs are edited), users relying on screen readers won't notice because the visual change happens outside their keyboard focus.
**Action:** Always use an explicitly injected `aria-live="polite"` announcer region to proactively notify screen reader users when decoupled content states change significantly.

## 2026-08-06 - Direct Input Focus for Edit Actions
**Learning:** When a user clicks an 'Edit Inputs' or 'Back to Form' jump link from a result container, linking to the top-level section container (e.g., `<section id="nozzle">`) requires them to manually press Tab or click again to focus the first input field to start editing. Additionally, if the page load hash handler aggressively applies `tabindex="-1"` to any targeted element to allow programmatic focus, it will inadvertently remove inherently focusable elements (like `<input>`) from the sequential keyboard tab order if they are the target.
**Action:** Always point 'Edit' jump links directly to the `id` of the first interactive input field (e.g., `<a href="#P0">`) to immediately focus the field and eliminate unnecessary user friction. Concurrently, when applying programmatic focus on page load, explicitly check `!target.matches('a[href], button, input, textarea, select, details, [tabindex]')` before applying `tabindex="-1"` to preserve the native tab order.

## 2026-08-14 - Native Hover Tooltip on Pattern Validation
**Learning:** Using the `title` attribute on input fields to supply custom error messages for `patternMismatch` (a common practice to override native tooltips) causes the browser to persistently display a native hover tooltip. This redundant tooltip obstructs the UI and provides a poor hover experience since the information is already conveyed via helper text and inline validation.
**Action:** Instead of using the `title` attribute, store custom validation messages in a `data-*` attribute (e.g., `data-pattern-error`) and update the JS validation logic to read from it. This prevents the browser from showing the intrusive native hover tooltip while still providing the custom message to the inline error UI.
## 2025-02-23 - Accessible Loading Animations
**Learning:** When adding CSS animated loading spinners (e.g., replacing static emojis during form submission), they can cause discomfort for users with vestibular sensitivities.
**Action:** Always include a `prefers-reduced-motion: reduce` fallback (via CSS media query or JS `window.matchMedia`) to revert to a static visual or remove the animation.
