## 2024-05-18 - Flask Exception Reflection XSS
**Vulnerability:** Reflected Cross-Site Scripting (XSS) in Flask API error handlers.
**Learning:** In Flask `api/index.py`, when a user input cannot be parsed (e.g. `float('<script>...')`), the standard `except Exception as e: return f"Error: {str(e)}"` pattern reflects the raw malicious input directly back into the `text/html` response.
**Prevention:** Always use `markupsafe.escape()` when returning exception strings or any user-controlled data directly as HTML in Flask route responses.

## 2024-05-18 - Logical DoS in Computational Loops
**Vulnerability:** Application-level Denial of Service (DoS) due to unbounded array processing.
**Learning:** In Flask `api/index.py`, taking a comma-separated string of numbers (`machs`), parsing it into a list, and passing it to computationally expensive scientific operations (e.g. `ObliqueShock.plot_polar`) without limiting the size of the array or input string allows a user to trivially exhaust server resources (CPU/memory) by sending thousands of items.
**Prevention:** Always validate and bound the size of user-provided arrays or strings before processing them, especially when passed to expensive loops or scientific computing functions. Set `app.config['MAX_CONTENT_LENGTH']` globally, and strictly bound logical length limits within individual routes.

## 2026-03-28 - Unhandled Type Casting and Logical Math Exceptions (Denial of Service)
**Vulnerability:** 500 Internal Server Errors and unhandled numerical exceptions (ZeroDivisionError, ValueError) from unvalidated physical inputs.
**Learning:** In Flask applications like `api/index.py` that interface with scientific solvers (`rankine/`), blindly casting `request.form.get()` directly to `float` without a `try-except` block, and blindly passing these floats into physics routines without bounds checking (e.g., negative time, negative areas, Mach < 1.0) leads to unhandled Python exceptions. Attackers can trigger continuous 500 errors or solver crashes (logical DoS) by submitting mathematically invalid or non-numeric string payloads.
**Prevention:** Always wrap type casting of user input in a `try...except ValueError` block. Always explicitly validate the physical/logical bounds of numbers (`> 0`, `>= 1.0`) *before* passing them to downstream numerical solvers, failing gracefully with a `400 Bad Request` if invalid.
## 2026-03-29 - Missing Security Headers
**Vulnerability:** Defense in Depth: Missing standard HTTP security headers.
**Learning:** In Flask `api/index.py`, the responses lacked standard security headers such as `X-Content-Type-Options`, `X-Frame-Options`, and `Content-Security-Policy`. This makes the application more susceptible to MIME sniffing and clickjacking attacks.
**Prevention:** Implement an `@app.after_request` decorator in the Flask app to automatically append security headers to all outgoing responses. This is a crucial layer of defense in depth.
