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

## 2026-04-03 - HTML Number Inputs Reject Decimals By Default
**Learning:** Native `<input type="number">` elements have an implicit `step="1"`, meaning they reject floating-point numbers and trigger an invalid state (showing an error border if styled) when users try to enter decimals. For physical calculations where decimals are common (like pressures or areas), this causes confusing validation errors.
**Action:** Always explicitly set `step="any"` (or a specific decimal step like `step="0.01"`) on `<input type="number">` fields if non-integer values are valid inputs.
