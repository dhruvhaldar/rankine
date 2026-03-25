## 2024-05-18 - Flask Exception Reflection XSS
**Vulnerability:** Reflected Cross-Site Scripting (XSS) in Flask API error handlers.
**Learning:** In Flask `api/index.py`, when a user input cannot be parsed (e.g. `float('<script>...')`), the standard `except Exception as e: return f"Error: {str(e)}"` pattern reflects the raw malicious input directly back into the `text/html` response.
**Prevention:** Always use `markupsafe.escape()` when returning exception strings or any user-controlled data directly as HTML in Flask route responses.

## 2024-05-18 - Logical DoS in Computational Loops
**Vulnerability:** Application-level Denial of Service (DoS) due to unbounded array processing.
**Learning:** In Flask `api/index.py`, taking a comma-separated string of numbers (`machs`), parsing it into a list, and passing it to computationally expensive scientific operations (e.g. `ObliqueShock.plot_polar`) without limiting the size of the array or input string allows a user to trivially exhaust server resources (CPU/memory) by sending thousands of items.
**Prevention:** Always validate and bound the size of user-provided arrays or strings before processing them, especially when passed to expensive loops or scientific computing functions. Set `app.config['MAX_CONTENT_LENGTH']` globally, and strictly bound logical length limits within individual routes.
