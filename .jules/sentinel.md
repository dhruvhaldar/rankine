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

## 2026-04-03 - Hardcoded Debug Mode in Production
**Vulnerability:** Information Exposure and Remote Code Execution (RCE) via Werkzeug interactive debugger.
**Learning:** Hardcoding `app.run(debug=True)` in application entry points (`api/index.py`) is dangerous because if the file is accidentally executed or deployed in a way that triggers this block, it exposes the Werkzeug interactive debugger. This debugger allows arbitrary Python code execution from the browser, leading to full server compromise.
**Prevention:** Never hardcode `debug=True`. Always determine debug mode dynamically using environment variables (e.g., `os.environ.get('FLASK_DEBUG')`).
