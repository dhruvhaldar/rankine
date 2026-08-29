## 2026-05-09 - Fix missing CSRF protection on state-changing endpoints
**Vulnerability:** The Flask application lacked Cross-Site Request Forgery (CSRF) protection on computationally expensive `POST` endpoints (`/plot/*`). Although the app is stateless (no cookies), malicious sites could force users to execute arbitrary compute-heavy requests by submitting cross-origin forms, potentially leading to Application-Layer DoS.
**Learning:** In stateless applications without sessions, traditional CSRF tokens are difficult to implement. However, modern browsers reliably send `Origin` and `Referer` headers on cross-origin `POST` requests. We can implement a lightweight, OWASP-recommended defense by strictly validating these headers against the expected `request.host`. Furthermore, when aborting requests early in a `@app.before_request` hook, care must be taken to handle variables in the `g` object (like `g.csp_nonce`), as subsequent initialization hooks will be skipped, causing `AttributeError`s in `after_request` hooks if not accessed safely via `getattr()`.
**Prevention:** Always implement `Origin` / `Referer` validation on state-changing or expensive endpoints in stateless applications. Ensure that `after_request` hooks safely access the `g` object using `getattr()` with fallback values to prevent crashes when earlier hooks abort the request lifecycle.

## 2024-05-10 - Insufficient logging of security events
**Vulnerability:** The application was missing audit logs for security mechanisms, specifically rate limit violations, CSRF origin/referer mismatches, and oversized payload errors (413). Without these logs, it is difficult or impossible to identify and analyze attack attempts against the API.
**Learning:** Defense-in-depth mechanisms, while effective at preventing immediate exploitation, must also provide visibility. A silent failure pattern allows attackers to probe endpoints indefinitely without triggering alerts.
**Prevention:** Always add explicit logging (e.g., `logger.warning`) capturing relevant context (IP, path, headers) when security protections (rate limiting, CSRF validation, payload limits) reject a request.

## 2026-05-13 - Mitigate Log Injection (CRLF) via unescaped path and headers
**Vulnerability:** The application was vulnerable to Log Forging (CRLF Injection) because user-controllable input from `request.path` and header values (`Origin`, `Referer`) were written directly to `logger.warning` without sanitization. An attacker could embed `\r\n` characters in these fields to inject fake log entries, potentially confusing automated log analysis tools or hiding malicious activity.
**Learning:** Even built-in framework attributes like `request.path` and standard HTTP headers can contain unescaped newline characters. Standard Python logging does not automatically escape these.
**Prevention:** Always implement a dedicated string sanitization function (e.g., replacing `\n` and `\r` with their escaped representations `\\n` and `\\r`) and apply it to all user-controlled data before passing it to logging functions.

## 2024-05-14 - Fix rate limit bypass in memory eviction
**Vulnerability:** The in-memory rate limiter in `api/index.py` used `rate_limit_data.clear()` when the dictionary size exceeded 10000. An attacker could flood the server with requests from spoofed or distributed IPs to trigger the clear, resetting rate limits for all active users and allowing them to bypass the limit on their own IP.
**Learning:** Using a blunt `clear()` to prevent memory exhaustion in a dictionary-based rate limiter inadvertently creates a DoS vulnerability or rate limit bypass. When evicting elements to maintain a size limit, older elements should be removed iteratively instead of wiping the entire state.
**Prevention:** Instead of `.clear()`, safely pop the oldest entries (e.g., `while len(d) > limit: d.pop(next(iter(d)))`) when limits are reached to only remove the oldest tracked IPs.

## 2026-05-20 - Prevent Log Injection via Spoofed IP
**Vulnerability:** Log forging/CRLF injection through unsanitized `request.remote_addr`.
**Learning:** Even when `ProxyFix` is used, the resolved `request.remote_addr` originates from the `X-Forwarded-For` header, which is user-controlled. If an attacker injects newlines into this header, it could corrupt log files and hide malicious activity if logged unsanitized.
**Prevention:** Always wrap `request.remote_addr` (and any variables derived from it, like `client_ip`) in a sanitization function (e.g., `sanitize_for_log()`) before passing it to `logger` methods.

## 2026-05-31 - Fix swallowed HTTPException in global error handlers
**Vulnerability:** General `except Exception as e:` blocks in Flask routes swallow `werkzeug.exceptions.HTTPException` errors, causing them to return generic 500 internal server errors instead of the correct HTTP status codes (e.g., 400, 404, 429).
**Learning:** Catching a broad `Exception` in specific routes or middleware can unintentionally mask valid HTTP errors thrown by the framework or application logic, misleading clients and obscuring actual error conditions.
**Prevention:** Explicitly catch and re-raise `werkzeug.exceptions.HTTPException` before the broad `Exception` handler so Flask can handle and return the correct HTTP status codes appropriately.

## 2026-06-04 - Fix Host Header Injection / CSRF Bypass
**Vulnerability:** The application's stateless CSRF protection relied on comparing `Origin` or `Referer` headers against `request.host`. Because the application is behind a reverse proxy and uses `ProxyFix`, `request.host` is dynamically derived from the `X-Forwarded-Host` header, which is controllable by the user. An attacker could spoof the `X-Forwarded-Host` header to match their spoofed `Origin` header, bypassing the CSRF check and executing compute-heavy requests leading to DoS.
**Learning:** When using `ProxyFix` behind a proxy, `request.host` cannot be trusted as a security boundary for CSRF validation because it originates from the unauthenticated `X-Forwarded-Host` header. Additionally, automated reviewers may incorrectly flag functions (like `sanitize_for_log`) as "undefined" because they review the patch in isolation without full file context; always verify function definitions in the file (e.g., using `grep`) before altering a correct fix.
**Prevention:** Always implement defense-in-depth by explicitly validating `request.host` against an environment-configured allowlist (e.g., `ALLOWED_HOSTS`) before relying on it for sensitive security checks like CSRF validation.

## 2026-06-10 - Unhandled ValueError in urlparse for CSRF
**Vulnerability:** The CSRF validation logic in `api/index.py` used `urllib.parse.urlparse()` to parse the `Origin` and `Referer` headers. However, `urlparse` can raise a `ValueError` for malformed inputs (like invalid IPv6 addresses). If an attacker sends a malformed `Origin` or `Referer` header, the unhandled exception could lead to an internal server error (500) and expose internal stack traces or cause unexpected application behavior.
**Learning:** Functions that parse user-controlled input, including HTTP headers, can throw exceptions for malformed data. These exceptions must be explicitly caught and handled to prevent information leakage or DoS vulnerabilities.
**Prevention:** Always wrap parsing functions like `urlparse()` in a `try...except ValueError` block when operating on untrusted data, such as headers, and return a safe HTTP 400 response.
## 2026-06-26 - Add X-XSS-Protection header
**Vulnerability:** The application was missing the `X-XSS-Protection: 0` HTTP header. While this header is considered legacy, not explicitly setting it to `0` leaves applications vulnerable to side-channel attacks on older browsers where attackers can manipulate the built-in XSS auditor to block legitimate application scripts, leading to a denial of service or unexpected behavior.
**Learning:** Legacy browser XSS filters (which the `X-XSS-Protection` header originally controlled) are deprecated and have been known to introduce vulnerabilities rather than fix them. OWASP and MDN recommend explicitly disabling this feature by setting the value to `0`, relying instead on a robust Content-Security-Policy (CSP) for XSS defense.
**Prevention:** Always explicitly set `X-XSS-Protection: 0` in the security middleware or header configuration of web applications to ensure legacy XSS auditors are disabled.
## 2026-06-27 - Strengthen Cache-Control header
**Vulnerability:** The application used `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` to prevent caching of sensitive generated content. While `no-store` is strict, older or non-compliant shared caches might ignore it or process it incorrectly, potentially caching sensitive generated plots.
**Learning:** Adding the `private` directive provides defense-in-depth against shared caches (like proxies and CDNs), explicitly instructing them not to store the response, even if they fail to properly handle `no-store`.
**Prevention:** Always use comprehensive modern `Cache-Control` directives (including `private` alongside `no-store` and `no-cache`) for sensitive dynamic content to ensure maximum compatibility and strict enforcement across all types of caches.

## 2026-07-01 - Prevent Matplotlib version leakage in PNG metadata
**Vulnerability:** The application was leaking the Matplotlib version in the metadata of the generated PNG files. This information leakage could be used by attackers to fingerprint the backend stack and exploit known CVEs in that specific version.
**Learning:** By default, Matplotlib embeds its version in the `Software` metadata field of PNG files. This is unnecessary for functionality and increases the attack surface.
**Prevention:** Always explicitly override or remove unnecessary metadata (e.g., passing `metadata={'Software': None}`) when generating files with external libraries to prevent version leakage.
## 2026-07-02 - Prevent Ephemeral Secret Key Anti-Pattern\n**Vulnerability:** The Flask application was missing a `SECRET_KEY` configuration, meaning if sessions were later enabled or required by plugins, they would either fail or insecurely fallback to runtime-generated ephemeral keys, invalidating sessions on every restart or across multi-worker deployments.\n**Learning:** Relying on ephemeral random keys (e.g. `secrets.token_hex`) for `SECRET_KEY` in production creates unstable sessions and introduces security risks in distributed environments. The application should fail fast if a required secret is missing, rather than generating an unstable one.\n**Prevention:** Explicitly configure the `SECRET_KEY` from a secure environment variable (e.g., `os.environ.get('SECRET_KEY')`). If it's missing, leave it unset so the framework correctly fails securely upon session usage.

## 2026-07-07 - CSP Nonce Generation on Early Abort
**Vulnerability:** The application applied a CSP nonce generated in a `before_request` hook within an `after_request` hook. If a request was aborted early (e.g., due to a 403 or 400 error), the `before_request` hook might not run or global state might not be populated, causing `g.csp_nonce` to be an empty string. The CSP header would then be set with `nonce-`, which is an invalid directive and could potentially be bypassed or cause browser warnings.
**Learning:** Security header generation in `after_request` must be defensive against the possibility that `before_request` hooks were bypassed due to early aborts. Generating an invalid CSP directive weakens the policy.
**Prevention:** Conditionally construct the nonce directive (e.g., `nonce_directive = f" 'nonce-{csp_nonce}'" if csp_nonce else ""`) to gracefully degrade to standard non-nonce CSP rules (like `self`) if the nonce is missing.

## 2026-07-09 - Prevent Silent Failure on Payload Limit Rejections
**Vulnerability:** The application silently rejected excessively long inputs intended to prevent Application-Layer DoS. This silent failure pattern allowed attackers to probe endpoints indefinitely to find payload limits without triggering any security alerts or logs.
**Learning:** Security protections like payload limits, rate limiting, and CSRF validations must not only block malicious requests but also provide visibility into the attack. A silent rejection is only a partial defense.
**Prevention:** Always explicitly log (e.g., `logger.warning`) the rejection of requests by security controls, capturing relevant context such as the client IP and the endpoint being probed.

## 2026-07-10 - Sensitive Header Redaction in Audit Logs
**Vulnerability:** The application was not logging HTTP headers during security rejections, leading to poor observability. A naive implementation to fix this might dump `request.headers` directly into the logs. This introduces a critical vulnerability (CWE-532) by exposing sensitive headers like `Cookie` or `Authorization` in plaintext log files.
**Learning:** Security context enrichment must be carefully balanced with data privacy. While logging headers is highly useful for diagnosing attacks, it must never come at the cost of leaking session tokens or credentials. Furthermore, injecting dynamically formatted strings into `record.msg` within a `logging.Filter` can crash the logger if the injected content contains `%` characters and `record.args` is present.
**Prevention:** Always implement a redaction mechanism that explicitly strips or masks sensitive headers (e.g., 'Cookie', 'Authorization') before appending them to log records. If modifying `record.msg` in a filter, ensure any pending `record.args` are safely formatted first to prevent interpolation errors with untrusted header content.
## 2026-07-12 - Fix sensitive header redaction bypass in audit logs
**Vulnerability:** The logging filter intended to redact sensitive headers like `Cookie` and `Authorization` compared header names against a list of exact Title-Case strings (e.g., `'Cookie'`). Because HTTP headers are case-insensitive, an attacker (or standard browser) sending lowercase headers like `cookie:` bypassed the redaction logic. This allowed sensitive session credentials to be leaked in plaintext into the application logs (CWE-532).
**Learning:** In Flask/Werkzeug, converting `request.headers` to a standard Python dictionary via `dict(request.headers)` retains the original casing provided by the client. Security checks against these dictionary keys must not rely on exact case matching.
**Prevention:** Always perform case-insensitive comparisons (e.g., using `key.lower()`) when evaluating HTTP header names against security blocklists or redaction filters in Python dictionaries.

## 2026-07-12 - Allow HTTPException to fall through to global handlers
**Vulnerability:** The application was catching `BadRequest` and `RequestEntityTooLarge` exceptions directly in the route handlers and returning responses without proper logging. This caused a silent failure where payload limits or bad requests were rejected without being recorded in the security logs, blinding developers to probing attacks.
**Learning:** Catching specific `HTTPException`s within individual routes bypasses global error handlers (e.g., `@app.errorhandler(400)`) which are often responsible for centralized security logging and consistent response formatting.
**Prevention:** Always allow `HTTPException`s (or specific subclasses) to bubble up to global `@app.errorhandler` definitions to ensure security events are uniformly logged and handled across all endpoints.

## 2026-07-13 - Prevent Header Redaction Bypass via Casing/Padding
**Vulnerability:** The logging filter in `api/index.py` intended to redact sensitive headers like `Cookie` and `Authorization` compared header names against a list of exact Title-Case strings, or lower-cased them but didn't account for malformed HTTP keys. Since Flask/Werkzeug converts `request.headers` to a standard Python dictionary (`dict(request.headers)`) which preserves the original casing and padding provided by the client, an attacker could send headers like `cookie:` or ` Authorization ` to bypass the redaction filter. This allowed sensitive session credentials to be leaked in plaintext into the application logs (CWE-532).
**Learning:** In Flask/Werkzeug, iterating over `dict(request.headers)` retains the original raw string structure of the client's HTTP request keys. Security checks or redaction logic against these dictionary keys must not only rely on case-insensitive matching (`.lower()`), but must also explicitly strip trailing colons or whitespace (`.strip(' :')`), which are valid in HTTP requests and parsed natively by the WSGI server, bypassing strict character-matching filters.
**Prevention:** Always implement robust string normalization when dealing with user-supplied HTTP headers before performing security checks. Use `k.lower().strip(' :')` when redacting sensitive headers from log dictionaries to ensure variations do not bypass the filter.
## 2024-07-14 - Fix Silent Failure in 429 Error Handler
**Vulnerability:** 429 error handler was silently returning a response without logging the request details.
**Learning:** Failing to log rate limit rejections creates a silent failure pattern that allows attackers to probe endpoints without triggering alerts.
**Prevention:** Always add explicit logging capturing context like IP and path for all security-related error handlers.
## 2026-07-20 - Prevent Header Logging Bypass via Payload Injection
**Vulnerability:** The logging filter in `api/index.py` used a simple string match (`if "Headers:" not in record.getMessage()`) to prevent appending headers multiple times. An attacker could bypass this by injecting the string `Headers:` into the request payload (e.g., in the requested URL path like `/Headers:`), which gets formatted into the log message. This tricks the filter into skipping header logging, blinding the audit logs.
**Learning:** Relying on simple string inclusion checks on user-controllable log messages to track internal state creates injection vulnerabilities that can bypass security mechanisms.
**Prevention:** Use a dedicated boolean flag on the log record object (e.g., `getattr(record, "_headers_appended", False)`) to securely track state instead of relying on the mutable and user-controllable log message text.

## 2026-07-20 - Fix Header Redaction Bypass for all Whitespaces
**Vulnerability:** The previous header redaction mechanism only stripped spaces and colons (`.strip(' :')`). Attackers could bypass redaction by padding sensitive HTTP headers like `Cookie` or `Authorization` with other whitespace characters (e.g., `	`, `
`), leading to credentials leaking in plaintext to the audit logs.
**Learning:** HTTP headers can be parsed with varied whitespace characters. Relying on a subset of whitespace for stripping leaves a bypass vector open.
**Prevention:** Use a comprehensive list of whitespace characters (e.g., `'
:'`) when normalizing HTTP headers for security filtering.
## 2024-03-22 - Fix Global Error Handler Bypass
**Vulnerability:** Global error handlers (which include critical security logging) were being bypassed because endpoints returned error tuples (e.g. `return "Error...", 400`) instead of raising `HTTPException`s.
**Learning:** In Flask/Werkzeug, returning a tuple directly from a view or `before_request` hook circumvents registered `@app.errorhandler` hooks for that HTTP status code. This breaks centralized security logging and defense-in-depth measures tied to those handlers.
**Prevention:** Always raise explicit Werkzeug exceptions (e.g. `raise BadRequest(...)`) instead of returning error tuples so that global error handling logic is consistently applied to all failure cases.
## 2026-07-22 - Prevent Null-Byte Log Injection
**Vulnerability:** The `sanitize_for_log` function successfully sanitized CRLF characters but failed to account for null bytes (`\x00`).
**Learning:** Injections using null bytes can cause premature log message truncation in underlying C-based logging systems (like syslog or fluentd), allowing attackers to hide payloads or bypass subsequent audit filters.
**Prevention:** Always explicitly escape null bytes (e.g., `.replace('\x00', '\\x00')`) when creating custom log string sanitization utilities.
## 2026-07-30 - Reflected XSS in Flask Error Handlers
**Vulnerability:** Flask defaults Content-Type to text/html for string response tuples from error handlers. Returning e.description unescaped allows Reflected XSS.
**Learning:** Relying on default content types when returning exception messages directly can expose the application to XSS via unsanitized URLs in 404 handlers, etc.
**Prevention:** Always wrap returned error messages in escape() from markupsafe when returning string response tuples from Flask error handlers.

## 2026-08-05 - Prevent Terminal Log Injection
**Vulnerability:** The `sanitize_for_log` function failed to sanitize ANSI escape characters (\x1b) and backspaces (\b).
**Learning:** Unsanitized terminal escape sequences in logs can be parsed by terminal emulators, allowing attackers to visually erase, recolor, or spoof log entries to cover their tracks.
**Prevention:** Explicitly escape all terminal control characters (e.g., \x1b, \b) alongside CRLF and null bytes in logging sanitization functions.
## 2026-08-08 - Rate Limiter Clock Manipulation
**Vulnerability:** The rate limiter relied on `time.time()`, which is vulnerable to system clock adjustments (e.g., NTP syncing). A clock jump forward could expire all current rate limits early (bypassing the protection), while a jump backward could lock out users for extended periods (Denial of Service).
**Learning:** Relying on system clock adjustments in time-based security controls can lead to unpredictable lockouts or limit bypasses.
**Prevention:** Always use `time.monotonic()` for measuring elapsed time in rate limiters and session timeouts, as it provides a strictly increasing time reference immune to system clock changes.
## 2024-10-24 - Null-byte Header Redaction Bypass
**Vulnerability:** Redaction logic for HTTP headers in Flask was stripping whitespace but omitted null bytes, allowing an attacker to pass malformed headers like `Cookie\x00` which evaded redaction and leaked sensitive tokens to the logs.
**Learning:** Converting `request.headers` to a dictionary preserves trailing characters like null bytes that might bypass standard whitespace stripping.
**Prevention:** Always include the null byte `\x00` when stripping characters for case-insensitive header redaction logic.
## 2025-02-28 - Filter Injection Crash
**Vulnerability:** Injecting dynamically formatted strings directly into `record.msg` within a `logging.Filter` can crash the Python logger if the injected content contains `%` characters and `record.args` is present.
**Learning:** Manual interpolation like `record.msg % record.args` can raise TypeErrors or value errors. Safely resolve log messages inside filters by wrapping `record.getMessage()` in a `try...except`.
**Prevention:** Fall back to `str(record.msg)` on failure, and explicitly clear `record.args` to `()` before appending dynamic content to avoid DoS via malformed log messages.
