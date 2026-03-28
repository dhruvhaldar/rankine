
from flask import Flask, render_template, request, send_file
import io
import base64
from markupsafe import escape
import logging
import matplotlib
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
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB limit to prevent large payload DoS

logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plot/nozzle', methods=['POST'])
def plot_nozzle():
    try:
        try:
            P0 = float(request.form.get('P0', 101325))
            back_pressure = float(request.form.get('back_pressure', 95000))
            A_throat = float(request.form.get('A_throat', 0.05))
            A_exit = float(request.form.get('A_exit', 0.1))
        except ValueError:
            return "Error: Invalid physical parameters. Values must be numeric.", 400

        # Security: Validate physical parameter bounds
        if P0 < 0 or back_pressure < 0 or A_throat <= 0 or A_exit <= 0:
            return "Error: Invalid physical parameters. Values must be positive.", 400

        nozzle = CDNozzle(gamma=1.4, A_throat=A_throat, A_exit=A_exit)
        res = nozzle.solve(P0=P0, T0=300, back_pressure=back_pressure)

        fig = res.plot_distribution()

        # Save to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)

        return render_template('index.html', nozzle_plot=plot_url)
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs."

@app.route('/plot/shock_polar', methods=['POST'])
def plot_shock_polar():
    try:
        machs_str = request.form.get('machs', '2.0,3.0,5.0')

        # Security: Enforce limits on input to prevent logical DoS
        if len(machs_str) > 100:
            return "Error: Input too long.", 400

        try:
            machs = [float(m.strip()) for m in machs_str.split(',')]
        except ValueError:
            return "Error: Mach numbers must be numeric.", 400

        if len(machs) > 10:
            return "Error: Too many Mach numbers requested (max 10).", 400

        # Security: Ensure Mach numbers are physically valid for shock polar
        if any(m < 1.0 for m in machs):
            return "Error: Mach numbers must be >= 1.0.", 400

        fig = ObliqueShock.plot_polar(mach_numbers=machs, gamma=1.4)

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)

        return render_template('index.html', polar_plot=plot_url)
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs."

@app.route('/plot/shock_tube', methods=['POST'])
def plot_shock_tube():
    try:
        try:
            time = float(request.form.get('time', 0.25))
        except ValueError:
            return "Error: Time must be numeric.", 400

        # Security: Validate simulation time bounds
        if time < 0 or time > 100:
            return "Error: Time must be between 0 and 100 seconds.", 400

        driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
        driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}

        tube = ShockTube(driver, driven, gamma=1.4)
        tube.solve(time=time)

        fig = tube.plot_properties()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)

        return render_template('index.html', tube_plot=plot_url)
    except Exception as e:
        logger.error('Operation failed', exc_info=True)
        return "Error: An error occurred during calculation. Please check your inputs."

# For local testing
if __name__ == '__main__':
    app.run(debug=True)
