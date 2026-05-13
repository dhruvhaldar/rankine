
from flask import Flask, render_template, request, send_file, g
import io
import base64
import secrets
from werkzeug.exceptions import RequestEntityTooLarge, BadRequest
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import matplotlib
import math
import time
from collections import defaultdict
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Import Rankine modules
# We need to make sure 'rankine' is in path. Vercel root is project root.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rankine.isentropic import CDNozzle
from rankine.shocks import ObliqueShock
from rankine.unsteady import ShockTube

app = Flask(__name__, template_folder='../templates')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB limit to prevent large payload DoS

logger = logging.getLogger(__name__)

def sanitize_for_log(val):
    """Sanitize string for logging to prevent CRLF injection."""
    if not isinstance(val, str):
        val = str(val)
    return val.replace('\n', '\\n').replace('\r', '\\r')

# Security: In-memory rate limiter to prevent Application-Layer DoS
# Limits requests to prevent abuse of computationally expensive endpoints
rate_limit_data = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 30

@app.before_request
def rate_limiter():
    # Only limit POST requests (computational endpoints)
    if request.method == 'POST':
        current_time = time.time()

        # Security: Prevent memory exhaustion from too many unique IPs
        # Periodically evict stale IPs to prevent rate-limit bypass from blunt clear()
        if len(rate_limit_data) > 10000:
            for ip in list(rate_limit_data.keys()):
                rate_limit_data[ip] = [t for t in rate_limit_data[ip] if current_time - t < RATE_LIMIT_WINDOW]
                if not rate_limit_data[ip]:
                    del rate_limit_data[ip]
            if len(rate_limit_data) > 10000:
                rate_limit_data.clear()

        client_ip = request.remote_addr

        # Clean up old requests outside the window
        rate_limit_data[client_ip] = [t for t in rate_limit_data[client_ip] if current_time - t < RATE_LIMIT_WINDOW]

        if len(rate_limit_data[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
            logger.warning(f"Security: Rate limit exceeded for IP {client_ip} on endpoint {sanitize_for_log(request.path)}")
            return "Error: Too many requests. Please try again later.", 429

        rate_limit_data[client_ip].append(current_time)

@app.before_request
def csrf_protect():
    # Security: CSRF protection for state-changing POST requests
    # Validates Origin or Referer header against expected host to prevent cross-site request forgery
    if request.method == "POST":
        origin = request.headers.get("Origin")
        referer = request.headers.get("Referer")

        from urllib.parse import urlparse
        expected_host = request.host

        if origin:
            if urlparse(origin).netloc != expected_host:
                logger.warning(f"Security: CSRF validation failed - Invalid Origin: {sanitize_for_log(origin)} from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
                return "Error: Invalid Origin.", 403
        elif referer:
            if urlparse(referer).netloc != expected_host:
                logger.warning(f"Security: CSRF validation failed - Invalid Referer: {sanitize_for_log(referer)} from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
                return "Error: Invalid Referer.", 403
        else:
            logger.warning(f"Security: CSRF validation failed - Missing Origin and Referer from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
            return "Error: Missing Origin or Referer header.", 403

@app.before_request
def generate_csp_nonce():
    g.csp_nonce = secrets.token_hex(16)

@app.context_processor
def inject_csp_nonce():
    return dict(csp_nonce=g.csp_nonce)

@app.after_request
def add_security_headers(response):
    # Security: Defense in depth via HTTP headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    # Use nonce for inline scripts to prevent XSS while allowing valid functionality
    csp_nonce = getattr(g, 'csp_nonce', '')
    response.headers['Content-Security-Policy'] = f"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'nonce-{csp_nonce}'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests;"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), fullscreen=()'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(e):
    return "Error: The requested URL was not found on the server.", 404

@app.errorhandler(400)
def bad_request(e):
    return "Error: Bad request.", 400

@app.errorhandler(405)
def method_not_allowed(e):
    return "Error: The method is not allowed for the requested URL.", 405

@app.errorhandler(413)
def request_entity_too_large(e):
    logger.warning(f"Security: Request payload too large (413) from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
    return "Error: Request payload is too large.", 413

@app.errorhandler(429)
def too_many_requests(e):
    return "Error: Too many requests. Please try again later.", 429

@app.errorhandler(500)
def internal_server_error(e):
    return "Error: An internal server error occurred.", 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plot/nozzle', methods=['POST'])
def plot_nozzle():
    try:
        try:
            P0_str = str(request.form.get('P0', '101325'))
            back_pressure_str = str(request.form.get('back_pressure', '95000'))
            A_throat_str = str(request.form.get('A_throat', '0.05'))
            A_exit_str = str(request.form.get('A_exit', '0.1'))

            # Security: Prevent DoS from parsing massive strings
            if max(len(P0_str), len(back_pressure_str), len(A_throat_str), len(A_exit_str)) > 100:
                return "Error: Input too long.", 400

            P0 = float(P0_str)
            back_pressure = float(back_pressure_str)
            A_throat = float(A_throat_str)
            A_exit = float(A_exit_str)

            # Security: Prevent NaN/Inf validation bypass
            if not (math.isfinite(P0) and math.isfinite(back_pressure) and math.isfinite(A_throat) and math.isfinite(A_exit)):
                raise ValueError("Values must be finite.")
        except ValueError:
            return "Error: Invalid physical parameters. Values must be numeric and finite.", 400

        # Security: Validate physical parameter bounds
        if P0 <= 0 or back_pressure <= 0 or A_throat <= 0 or A_exit <= 0:
            return "Error: Invalid physical parameters. Values must be strictly positive.", 400

        # Security: Ensure Converging-Diverging Nozzle geometry is physically valid
        if A_exit < A_throat:
            return "Error: Invalid physical parameters. Exit Area must be >= Throat Area.", 400

        # Security: Prevent logical DoS and OverflowError in solvers
        if P0 > 1e7 or back_pressure > 1e7 or A_throat > 100 or A_exit > 100:
            return "Error: Invalid physical parameters. Values exceed maximum bounds.", 400

        if A_exit / A_throat > 100:
            return "Error: Area ratio (Exit/Throat) must be <= 100.", 400

        nozzle = CDNozzle(gamma=1.4, A_throat=A_throat, A_exit=A_exit)
        res = nozzle.solve(P0=P0, T0=300, back_pressure=back_pressure)

        fig = res.plot_distribution()

        try:
            # Save to buffer
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        finally:
            plt.close(fig)

        return render_template('index.html', nozzle_plot=plot_url)
    except BadRequest:
        return "Error: Bad request.", 400
    except RequestEntityTooLarge:
        logger.warning(f"Security: Request payload too large (413) from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
        return "Error: Request payload is too large.", 413
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs.", 500

@app.route('/plot/shock_polar', methods=['POST'])
def plot_shock_polar():
    try:
        machs_str = request.form.get('machs', '2.0,3.0,5.0')

        # Security: Enforce limits on input to prevent logical DoS
        if len(machs_str) > 100:
            return "Error: Input too long.", 400

        try:
            machs = [float(m.strip()) for m in machs_str.split(',')]

            # Security: Prevent NaN/Inf validation bypass
            if not all(math.isfinite(m) for m in machs):
                raise ValueError("Mach numbers must be finite.")
        except ValueError:
            return "Error: Mach numbers must be numeric and finite.", 400

        if len(machs) > 10:
            return "Error: Too many Mach numbers requested (max 10).", 400

        # Security: Ensure Mach numbers are physically valid for shock polar
        if any(m < 1.0 for m in machs):
            return "Error: Mach numbers must be >= 1.0.", 400

        # Security: Prevent mathematical overflow and DoS in numerical solvers
        if any(m > 100.0 for m in machs):
            return "Error: Mach numbers must be <= 100.0.", 400

        fig = ObliqueShock.plot_polar(mach_numbers=machs, gamma=1.4)

        try:
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        finally:
            plt.close(fig)

        return render_template('index.html', polar_plot=plot_url)
    except BadRequest:
        return "Error: Bad request.", 400
    except RequestEntityTooLarge:
        logger.warning(f"Security: Request payload too large (413) from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
        return "Error: Request payload is too large.", 413
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs.", 500

@app.route('/plot/shock_tube', methods=['POST'])
def plot_shock_tube():
    try:
        try:
            time_str = str(request.form.get('time', '0.25'))

            # Security: Prevent DoS from parsing massive strings
            if len(time_str) > 100:
                return "Error: Input too long.", 400

            time = float(time_str)

            # Security: Prevent NaN/Inf validation bypass
            if not math.isfinite(time):
                raise ValueError("Time must be finite.")
        except ValueError:
            return "Error: Time must be numeric and finite.", 400

        # Security: Validate simulation time bounds
        if time <= 0 or time > 100:
            return "Error: Time must be strictly positive and less than or equal to 100 seconds.", 400

        driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
        driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}

        tube = ShockTube(driver, driven, gamma=1.4)
        tube.solve(time=time)

        fig = tube.plot_properties()

        try:
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        finally:
            plt.close(fig)

        return render_template('index.html', tube_plot=plot_url)
    except BadRequest:
        return "Error: Bad request.", 400
    except RequestEntityTooLarge:
        logger.warning(f"Security: Request payload too large (413) from IP {request.remote_addr} on endpoint {sanitize_for_log(request.path)}")
        return "Error: Request payload is too large.", 413
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs.", 500

# For local testing
if __name__ == '__main__':
    # Security: Use environment variable instead of hardcoded debug=True
    # to prevent Werkzeug interactive debugger exposure in production
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
