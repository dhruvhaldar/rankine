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
