## 2024-05-24 - Manual Focus Styles Needed in Raw HTML Templates
**Learning:** When working with raw HTML templates that lack a framework-provided CSS reset (like Tailwind or Bootstrap), native focus styles are often inadequate or inconsistent across browsers. This repository required manual `:focus-visible` styles to ensure keyboard accessibility. Additionally, raw HTML inputs with `width: 100%` and `padding` need `box-sizing: border-box` to prevent layout overflow.
**Action:** Always verify keyboard navigation and focus states in raw HTML projects, and manually add `outline`, `outline-offset`, and `box-sizing` if a CSS reset is absent.
## 2024-10-25 - Provide Feedback on Synchronous Form Submissions
**Learning:** In traditional POST-back templates without AJAX/fetch (like simple Flask apps), expensive calculations cause the browser to "hang" while waiting for the response. Without loading feedback, users often click submit multiple times, leading to redundant calculations and frustration.
**Action:** Always add simple JS to forms that trigger heavy backend processing to disable the submit button and change its text to indicate a loading state (e.g., "Calculating..."). Also, remember to add proper `button:disabled` CSS styles to give visual feedback that the element is inactive.
## 2024-11-20 - Expose Backend Constraints in UI via HTML Attributes and Helper Text
**Learning:** When backend endpoints have implicit constraints (like max length for DoS protection or non-negative requirements for physical quantities), the frontend UI must explicitly communicate these constraints to the user before form submission. Without client-side validation, users experience unstyled plain-text server errors, which is a poor experience.
**Action:** Always add HTML validation attributes (`min`, `max`, `maxlength`) and clear helper text (e.g., `<small>` tags inside `<label>`) to explicitly display backend constraints in the frontend UI.
## 2024-05-24 - Mirroring Backend Array Length Constraints
**Learning:** In Flask/HTML forms, if a text input expects a comma-separated array (like Mach numbers), it's important to mirror the backend array length limits (e.g., max 10 items) directly on the client side using the HTML `pattern` attribute and a clear `title` description. This provides instant visual feedback and prevents unstyled server error responses from being the first time users learn about the limit.
**Action:** When implementing new form inputs that expect arrays or delimited strings, always use HTML `pattern` validation to enforce size/length limits and provide helpful tooltips/error messages instead of relying entirely on backend validation.

## 2026-03-01 - Prevent Context Loss on Full-Page Form Posts
**Learning:** Relying on traditional form POSTs in a single long page causes disorienting scroll resets, which drops the user back to the top of the page after they submit a form midway down.
**Action:** When working with multiple forms on a long page that require full page reloads, append URL anchor hashes (e.g., `#section-id`) to the form `action` URLs to automatically scroll the user back to the relevant section and preserve their context.

## 2026-03-05 - Maintain Screen Reader Focus During Form Submission
**Learning:** When adding JavaScript to disable a submit button during form submission (to prevent double-posts and show a loading state), using the native `disabled` attribute (`btn.disabled = true`) drops the keyboard and screen reader focus. This causes screen readers to completely fail to announce the "Calculating..." feedback text because the element they were focused on became inactive.
**Action:** Use `aria-disabled="true"` instead of the native `disabled` attribute, manually prevent duplicate form submissions in the `submit` event handler (`e.preventDefault()`), and add `aria-live="polite"` to the button. This visually disables the button using CSS (`button[aria-disabled="true"]`) while preserving focus so the screen reader successfully announces the state change.

## 2026-03-31 - Aligning Frontend Validation with Backend Constraints
**Learning:** In traditional server-rendered applications, returning plain-text 400 Bad Request errors for validation failures creates a disorienting user experience. Users lose context and have to click 'Back' to fix their input.
**Action:** Always ensure that frontend HTML validation attributes (`min`, `max`, `pattern`) and inline helper texts strictly align with backend security constraints (like logical DoS protection limits or physical bounds) to catch input errors client-side before submission.

## 2026-04-01 - Enhance Form Validation with Inline Visual Feedback
**Learning:** Relying solely on native browser submit-time popups for HTML form validation (like `min`, `max`, `pattern`) can be frustrating because the user doesn't realize their input is invalid until they attempt to submit. This is particularly problematic in forms where inputs have pre-filled valid defaults.
**Action:** Use CSS pseudo-classes like `:invalid` and `:focus-visible:invalid` to provide immediate, inline visual feedback (e.g., a red border and subtle background color) to inputs when they violate HTML validation constraints. This allows users to catch and correct errors as they type.

## 2026-04-02 - Inline validation for interdependent fields
**Learning:** Interdependent field validation (e.g. Exit Area must be >= Throat Area) handled exclusively by backend APIs creates a poor UX because it results in unstyled text errors on submission and drops user context.
**Action:** Always link physically interdependent inputs directly on the frontend using inline `oninput` handlers to manipulate HTML5 constraint attributes (like `min` or `max`). This leverages existing `:invalid` CSS rules for immediate visual feedback before submission.

## 2026-04-06 - Allow decimal numbers in physical inputs
**Learning:** Native `<input type="number">`, elements implicitly use `step="1"`, rejecting valid decimal values. This limits floating-point numbers unless `step="any"` or a specific decimal is applied.
**Action:** Always add `step="any"` to number inputs representing continuous physical data to avoid unstyled browser validation errors and provide better UX.

## 2026-04-10 - Provide Explicit Empty States for Generated Content
**Learning:** In templates where content (like charts or images) is generated dynamically after a form submission, omitting an explicit empty state causes the page layout to feel sparse or broken on initial load. Users may be confused about where the result will appear or what action is required to trigger it.
**Action:** Always provide explicit, visually distinct empty states (e.g., a dashed border container with helpful call-to-action text) in `{% else %}` template blocks. This stabilizes the layout, sets user expectations, and guides them towards their first action.

## 2026-04-15 - Visual Hierarchy and Micro-interactions in Forms
**Learning:** In forms, putting helper text on the same line as the label can make scanning difficult, especially for long forms. Micro-interactions like `:active` scale states on buttons and transitions on input states can greatly improve the perceived responsiveness of traditional server-rendered applications, providing the tactile feedback that users expect from modern SPAs.
**Action:** When styling forms, always ensure a clear visual hierarchy by placing helper text on its own line with reduced visual weight. Additionally, include subtle CSS transitions on interactive elements (inputs, buttons) to soften state changes and provide immediate tactile feedback upon interaction.

## 2026-04-20 - Expose Required Fields Visually Without Redundant Announcements
**Learning:** Adding explicit visual indicators for required fields (like a red asterisk) is important for UX, but simply inserting text like "*" can cause screen readers to read "star" aloud unnecessarily, cluttering the experience, particularly when the `<input>` element already correctly uses the `required` attribute.
**Action:** When adding explicit visual indicators for required fields to the UI, wrap the indicator in an unstyled HTML tag with `aria-hidden="true"` (e.g., `<span aria-hidden="true">*</span>`). This ensures the visual indicator is hidden from assistive technologies, which will already correctly announce the requirement based on the native `required` attribute.

## 2026-05-15 - Make URL Anchor Hashes Accessible to Screen Readers
**Learning:** Using URL anchor hashes (e.g., `#section-id`) to prevent scroll resets during full-page form POSTs is good for visual context, but without explicit focus management, keyboard and screen reader focus defaults back to the top of the document after the page reloads.
**Action:** When using URL anchor hashes for redirecting after a form submission, ensure the target element (usually a container `<div>` or `<section>`) has `tabindex="-1"`. This allows the browser to programmatically shift focus to that container upon reload, ensuring keyboard and assistive technology users maintain their proper context.

## 2026-05-18 - Continuous Visual Feedback for Length-Constrained Inputs
**Learning:** When inputs have strict `maxlength` constraints (e.g., to prevent logical DoS from processing long array strings), relying solely on the browser silently refusing more keystrokes is a frustrating UX. Users don't know why they can't type or how close they are to the limit.
**Action:** When implementing an input with a `maxlength` attribute, always pair it with a dynamic character counter (e.g., `X / 100 characters`) updated via an inline `oninput` handler. Use `aria-live="polite"` on the counter to ensure screen readers also announce the changing length without interrupting the user.

## 2026-06-01 - Enhance Screen Reader Accessibility Tree with Semantic Landmarks
**Learning:** Replacing generic `<div>` tags with semantic HTML landmarks (like `<main>` and `<section>`) significantly improves the accessibility tree for screen readers, allowing users to easily navigate to distinct regions of the page. Combining `<section>` with `aria-labelledby` pointing to the section's heading ID explicitly names the region without relying on visual structure alone.
**Action:** When structuring raw HTML layouts, prefer semantic landmarks (`<main>`, `<section>`, `<aside>`, `<nav>`) over generic `<div>`s. Retain existing layout classes (e.g., `class="container"`) on the new tags to avoid visual CSS regressions, and use `aria-labelledby` to associate regions with their visible headings.

## 2026-06-15 - Initialize Dynamic UI States for Autofilled Forms
**Learning:** When updating character counters or other dynamic UI elements via `oninput` handlers, the initial page load may leave the UI out of sync if the browser autofills the input or restores cached data. The counter might say "0 / 100" even when there's text in the field.
**Action:** When initializing dynamic UI states linked to input fields (like character counters), always manually dispatch an `input` event on page load (e.g., `element.dispatchEvent(new Event('input', { bubbles: true }))`) to ensure the state immediately and accurately reflects the input's current value.

## 2026-06-20 - Improve Typography for Scientific Units
**Learning:** In scientific or technical interfaces, plain text representations of units and variables (like `P0` or `m2`) look unpolished and can be less readable than proper notation.
**Action:** Use proper HTML entities (e.g., `<sub>` for subscripts, `&sup2;` for superscripts) for physical variables and units to improve readability and visual polish without requiring custom CSS.

## 2026-06-25 - Provide Fallback Placeholders for Pre-filled Inputs
**Learning:** When form inputs are pre-filled with valid default values, users might clear the input and then forget the expected format or unit. Relying solely on `value` attributes without `placeholder` attributes leads to a loss of continuous guidance if the input is cleared.
**Action:** When pre-filling form inputs with default values, always include a matching `placeholder` attribute (e.g., `placeholder="e.g., 101325"`) as a fallback to ensure continuous context and guidance is provided even if the user deletes the content.

## 2026-07-01 - Force Proper Keypads for Physical Data on Mobile
**Learning:** Native `<input type="number">` on mobile devices (like iOS Safari) often defaults to a numeric keypad that lacks a decimal separator, or worse, shows a full alphanumeric keyboard. Since physical simulations frequently require floating-point numbers, this blocks users from inputting valid data like `0.05`.
**Action:** Always add `inputmode="decimal"` to number inputs representing continuous physical data to guarantee that mobile users are presented with a numeric keypad that includes a decimal separator.

## 2026-07-05 - Connect Screen Reader Focus to Dynamic Context
**Learning:** Character counters are visually useful, but screen reader users typing in the field only hear the number of characters updating (due to `aria-live`). They don't hear the *context* (e.g., "Max 100 characters") unless they happen to navigate to the counter element first.
**Action:** When using isolated character counters or helper text, always use `aria-describedby` on the `<input>` element pointing to the `id` of the descriptive text or counter container. This ensures the screen reader announces the full context when the user first focuses the input.

## 2026-07-06 - Auto-Select Pre-filled Inputs to Reduce Friction
**Learning:** In forms heavily reliant on pre-filled numerical data (e.g., physical defaults like 101325), failing to auto-select the text upon focus introduces significant UX friction. Users are forced to manually backspace or highlight long numbers to enter their own data.
**Action:** When working with forms populated by continuous numerical defaults, always attach a `focus` event listener that uses `setTimeout(() => this.select(), 0)` to automatically highlight the entire input value. This allows users to instantly overwrite the default value with a single keystroke.

## 2026-07-10 - Preserve User Input Across Full-Page Submissions
**Learning:** In applications using full-page POST submissions rather than AJAX, users experience intense frustration if they submit a form, hit an error (e.g., rate limit, network failure, or unhandled validation), and lose all their typed data. If the backend cannot reliably re-render the form with the submitted values, the data is permanently lost.
**Action:** Use client-side `sessionStorage` to save form input values on the `input` event and restore them upon `DOMContentLoaded`. This ensures that even if a full page reload occurs or an unhandled error drops the backend context, the user's hard work is preserved and instantly recovered.

## 2026-07-10 - Securely Implementing sessionStorage for Form State
**Learning:** While `sessionStorage` is excellent for preserving form data across full-page reloads, naive implementations (`document.querySelectorAll('input')`) can cause critical regressions. Using empty IDs as storage keys overwrites unrelated elements, and failing to clear the storage upon successful form submission permanently forces stale data on users, severely degrading the UX.
**Action:** When implementing `sessionStorage` preservation, strictly filter out inputs without IDs, exclude incompatible types (`hidden`, `submit`, `button`, `checkbox`, `radio`), and always hook into the `submit` event to explicitly `sessionStorage.removeItem()` for the submitted form's inputs, ensuring a clean slate for future interactions.

## 2024-04-27 - Scientific Form Autocomplete
**Learning:** In scientific web tools containing heavy arrays of complex inputs (e.g., pressure ratios, nozzle areas) paired with inline helper text, native browser autocomplete history often visually overlaps and obscures critical context limits. When the tool includes its own state preservation mechanism (like `sessionStorage`), the default browser autofill behavior becomes redundant and actively detrimental to the user experience.
**Action:** Always add `autocomplete="off"` to `<form>` tags in technical, calculation-heavy interfaces to ensure a clean UI and prevent browser history drop-downs from interfering with helper text or inline validation.

## 2025-04-28 - ARIA-Live Regions & Dynamically Injected Emojis
**Learning:** When updating `aria-live` regions (like a button's text changing to "⏳ Calculating..."), screen readers will announce the literal names of any dynamically injected emojis (e.g., "Hourglass with flowing sand"). This creates a verbose and confusing user experience.
**Action:** When dynamically injecting status updates containing decorative emojis via JavaScript, use `innerHTML` instead of `innerText` and wrap the emojis in `<span aria-hidden="true">` to ensure screen readers focus solely on the semantic text.

## 2024-05-18 - Form Submission Focus Management
**Learning:** In a server-rendered application where form submissions reload the page with results below the form, default behavior leaves focus at the top of the page, forcing screen reader and keyboard users to navigate past all the inputs again to reach the result.
**Action:** Append a hash fragment to the form's `action` URL (e.g., `#result`) and ensure the result container has a matching `id="result"` and `tabindex="-1"`. This causes the browser to natively scroll and shift focus directly to the new content upon load.

## 2024-05-18 - Prevent Accidental Number Input Scrolling
**Learning:** Browsers natively change the value of `<input type="number">` fields when scrolling the mouse wheel while the input is focused. In data-dense applications with long pages, users often click an input, type a value, and then scroll down to the submit button without explicitly clicking away to blur the input. This unintentionally alters their input value by several ticks, causing silent data corruption and frustrating recalculations.
**Action:** Prevent this hidden UX failure mode by attaching a global `wheel` event listener to the document that actively calls `.blur()` on `document.activeElement` if the focused element is a `type="number"` input.
