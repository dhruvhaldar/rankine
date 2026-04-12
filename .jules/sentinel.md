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

## 2026-03-30 - Float NaN/Inf Bound Validation Bypass
**Vulnerability:** Application-level Denial of Service (DoS) and unhandled mathematical exceptions caused by NaN or Infinity float representations.
**Learning:** In Python, converting string inputs like `"inf"`, `"-inf"`, or `"nan"` to `float()` succeeds without raising a `ValueError`. More dangerously, `float('nan') < 0` and `float('nan') <= 0` evaluate to `False`, bypassing basic comparative boundary checks (e.g. `if val < 0: raise Error`). This can lead to unhandled runtime exceptions (`RuntimeWarning: invalid value encountered in divide`) inside scientific computation solvers or infinite loop conditions, causing an application crash or resource exhaustion.
**Prevention:** Always validate parsed float inputs from web requests with `math.isfinite(val)` before proceeding with business logic or passing the data into mathematical functions.

## 2026-04-01 - Logical DoS via Invalid Area Ratio
**Vulnerability:** Application-level Denial of Service (DoS) and unhandled mathematical exceptions caused by physically invalid input combinations (e.g. Exit Area < Throat Area).
**Learning:** In Flask route `api/index.py`, while individual inputs (like `A_exit` and `A_throat`) were validated to be strictly positive numbers, their relationship was not validated. Providing `A_exit < A_throat` to the Converging-Diverging Nozzle solver caused the calculated area ratio to drop below `1.0`, triggering a `ValueError` inside the `scipy.optimize` root finder in `rankine/isentropic.py`. This bypassed individual bound checks and allowed an attacker to reliably crash the solver endpoint via logical errors.
**Prevention:** Always validate physical relationships between parameters (e.g., Exit Area must be >= Throat Area for CD nozzles) in the request handler before invoking downstream computational solvers, failing gracefully with a 400 Bad Request if the combination is invalid.

## 2026-04-02 - HSTS and Referrer-Policy Headers
**Vulnerability:** Defense in Depth: Missing Strict-Transport-Security (HSTS) and Referrer-Policy headers.
**Learning:** In Flask `api/index.py`, the responses lacked HSTS and Referrer-Policy headers. HSTS enforces secure (HTTPS) connections, preventing protocol downgrade attacks and cookie hijacking. Referrer-Policy prevents leaking sensitive URL information to cross-origin sites via the Referer header.
**Prevention:** Always include `Strict-Transport-Security` and `Referrer-Policy` headers in the `@app.after_request` decorator to strengthen the application's defense in depth.

## 2026-04-03 - Logical DoS via ZeroDivisionError
**Vulnerability:** Application-level Denial of Service (DoS) and unhandled mathematical exceptions caused by physically invalid zero inputs.
**Learning:** In Flask route `api/index.py`, the validation logic allowed `P0` and `back_pressure` to be exactly `0.0` (using `>= 0` indirectly by only blocking `< 0`). If `back_pressure` is `0.0`, the calculation `P0 / back_pressure` triggers a raw Python `ZeroDivisionError: float division by zero`, crashing the endpoint and allowing an attacker to cause resource exhaustion or continuous 500 Internal Server Errors via a logical DoS attack.
**Prevention:** Always ensure that physical parameter bounds check strictly block boundary edge cases (like `0.0`) when those values are subsequently used as denominators in physical calculations. Use strictly positive bounds (`<= 0`) where mathematically necessary.
## 2026-04-10 - Werkzeug Exception Leak and Unhandled HTTP Error 413
**Vulnerability:** Defense in Depth / Information Leak / Logical Error. Werkzeug's default `405 Method Not Allowed` and `413 Request Entity Too Large` return HTML containing server signature information. Additionally, `RequestEntityTooLarge` triggered by payload limit configurations is raised inside `try-except Exception` blocks when parsing `request.form`, leading to unnecessary `500 Internal Server Error` logs and responses instead of returning a correct 413.
**Learning:** Unhandled HTTP errors raised implicitly by Werkzeug (like 405 on invalid method, or 413 on payload size exceeding `MAX_CONTENT_LENGTH`) can leak server signatures if not caught. Catching generic exceptions (e.g. `except Exception:`) around `request.form` evaluation intercepts framework-level HTTP exceptions, leading to incorrect 500 errors.
**Prevention:** Use `@app.errorhandler(405)` and `@app.errorhandler(413)` globally to prevent framework information leakage. When `request.form` evaluation could trigger `werkzeug.exceptions.RequestEntityTooLarge`, specifically catch it and return a 413 response before falling back to generic 500 error handlers.

## 2026-04-11 - Broken CSP via Default-Src Fallback and Unsafe-Inline Risks
**Vulnerability:** Defense in Depth / XSS / Broken Functionality. Missing `script-src` directive in CSP causes `default-src 'self'` fallback, blocking legitimate inline JavaScript required for UI interactivity. Attempting to fix this by broadly adding `'unsafe-inline'` to `script-src` opens the application to severe Cross-Site Scripting (XSS) vulnerabilities.
**Learning:** When applying a Strict Content-Security-Policy to protect against XSS, failing to explicitly specify a `script-src` directive causes browsers to fall back to `default-src`. If `default-src` is `'self'`, all inline scripts (like `oninput` attributes and `<script>` blocks) are blocked, breaking the frontend functionality.
**Prevention:** Always explicitly define `script-src` in the CSP. To maintain strict XSS protection while allowing necessary frontend interactivity, generate a cryptographically secure random `nonce` per request (e.g., via `secrets.token_hex(16)`). Inject this nonce into the CSP header (`script-src 'self' 'nonce-{nonce}'`), replace all inline HTML event handlers (e.g., `oninput="..."`) with proper JS `addEventListener` logic inside a single `<script>` block, and apply the `nonce="..."` attribute to that script tag.
