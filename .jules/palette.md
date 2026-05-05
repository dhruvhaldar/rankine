## 2024-06-25 - Fix ambiguous download link text and add visual polish
**Learning:** Combating WCAG Link Purpose violations for identical visual labels (e.g., "Download Plot") using explicit, context-specific `aria-label` tags paired with `aria-hidden="true"` emojis creates an accessible, visually polished pattern.
**Action:** Always combine context-specific `aria-label` properties with `aria-hidden="true"` decorative elements to provide visual delight while maintaining screen reader clarity.
## 2023-10-27 - Programmatic Focus and Generic Regions
**Learning:** In forms that reload the page and use hash links to shift focus to results, applying `tabindex="-1"` appropriately moves browser focus but results in an ugly default focus ring wrapping the entire content area on most browsers. Additionally, applying `aria-label` to generic `<div>` tags is often ignored by screen readers.
**Action:** When creating focusable result containers, always apply `[tabindex="-1"]:focus { outline: none; }` to remove the default outline, and ensure the container has `role="region"` so that its `aria-label` is consistently announced when focus shifts.
