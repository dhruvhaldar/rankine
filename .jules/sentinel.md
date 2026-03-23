## 2024-05-18 - Flask Exception Reflection XSS
**Vulnerability:** Reflected Cross-Site Scripting (XSS) in Flask API error handlers.
**Learning:** In Flask `api/index.py`, when a user input cannot be parsed (e.g. `float('<script>...')`), the standard `except Exception as e: return f"Error: {str(e)}"` pattern reflects the raw malicious input directly back into the `text/html` response.
**Prevention:** Always use `markupsafe.escape()` when returning exception strings or any user-controlled data directly as HTML in Flask route responses.
