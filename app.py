import re
import xml.etree.ElementTree as ET

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

VALID_INPUT_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form['target']

    if not VALID_INPUT_REGEX.match(target):
        return "Error: Invalid input provided.", 400

    command = ['nmap', '-T4', '-F', '-oX', '-', target]

    scan_output = ""
    ports = []

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        xml_output = result.stdout
        root = ET.fromstring(xml_output)

        for port in root.findall('host/ports/port'):
            port_info = {
                 'protocol': port.get('protocol'),
                 'port': port.get('portid'),
                 'state': port.find('state').get('state'),
                 'service': port.find('service').get('name') if port.find('service') is not None else 'unknown'

            }
            ports.append(port_info)

    except FileNotFoundError:
        return "Error: 'nmap' command not found. Please install Nmap.", 500
    except subprocess.CalledProcessError as e:
        return f"Error during scan: {e.stderr}", 500

    return render_template('results.html', target=target, ports=ports)



if __name__ == '__main__':
    app.run(debug=True)


