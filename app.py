
import os
import re
import json
import uuid
import threading
import subprocess
import xml.etree.ElementTree as ET
import bugsnag
from bugsnag.flask import handle_exceptions
import shodan 
from config import SHODAN_API_KEY
import whois
import dns.resolver
from flask import Flask, render_template, request, redirect, url_for, jsonify


bugsnag.configure(
    api_key = "d08ce5abb162307f37a796fed94d9aba",
    project_root = "/app",
)


app = Flask(__name__)



RESULTS_FOLDER = 'results'
os.makedirs(RESULTS_FOLDER, exist_ok=True)

IPV4_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
DOMAIN_REGEX = re.compile(r"^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$")
VALID_INPUT_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$")


def run_scan_task(target, task_id):

    results = {
        'nmap': None,
        'whois': None,
        'dns': None,
        'shodan': None,
        'error': None
    }

    try:
        command = ['nmap', '-T4', '-A', '-oX', '-', target]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        xml_output = result.stdout
        ports = []
        if xml_output.strip():
            root = ET.fromstring(xml_output)
            for port in root.findall('host/ports/port'):
                port_info = {
                    'protocol': port.get('protocol'),
                    'port': port.get('portid'),
                    'state': port.find('state').get('state'),
                    'service': port.find('service').get('name') if port.find('service') is not None else 'unknown',
                    'product': port.find('service').get('product') if port.find('service') is not None else 'unknown'
                }
                ports.append(port_info)
            results['nmap'] = ports
    except Exception as e:
        results['error'] = f"Nmap scan failed: {str(e)}"

    if DOMAIN_REGEX.match(target):
        try:
            results['whois'] = whois.whois(target)
        except Exception:
            pass 
        
        try:
            dns_results = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            for rtype in record_types:
                answers = dns.resolver.resolve(target, rtype, raise_on_no_answer=False)
                if answers:
                    dns_results[rtype] = [str(rdata) for rdata in answers]
            results['dns'] = dns_results
        except Exception:
            pass 
    
    if IPV4_REGEX.match(target):
        try:
            api = shodan.Shodan(SHODAN_API_KEY)
            
            host_info = api.host(target)
            
            results['shodan'] = {
                'country': host_info.get('country_name', 'N/A'),
                'city': host_info.get('city', 'N/A'),
                'isp': host_info.get('isp', 'N/A'),
                'os': host_info.get('os', 'N/A'),
                'hostnames': host_info.get('hostnames', []),
                'ports': host_info.get('ports', [])
            }
        except shodan.APIError as e:
            results['shodan'] = {'error': str(e)}
        except Exception as e:
            results['shodan'] = {'error': f"An unexpected error occurred: {str(e)}"}

    filepath = os.path.join(RESULTS_FOLDER, f"{task_id}.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, default=str) 

handle_exceptions(app)

# --- Flask Routes --- 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test-crash')
def test_crash():
    """
    =>
    This route is designed to fail on purpose.
    Dividing by zero will raise a ZeroDivisionError.
    Bugsnag should catch this unhandled exception.
    
    """
    result = 1 / 0
    return f"This will never be seen: {result}"


@app.route('/scan', methods=['POST'])
def start_scan():
    target = request.form['target']
    if not VALID_INPUT_REGEX.match(target):
        return "Error: Invalid input provided.", 400

    task_id = str(uuid.uuid4())
    
    thread = threading.Thread(target=run_scan_task, args=(target, task_id))
    thread.start()

    
    return redirect(url_for('results_page', task_id=task_id))


@app.route('/results/<task_id>')
def results_page(task_id):

    return render_template('results.html', task_id=task_id)


@app.route('/status/<task_id>')
def scan_status(task_id):

    filepath = os.path.join(RESULTS_FOLDER, f"{task_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            results = json.load(f)
        return jsonify({'status': 'complete', 'data': results})
    else:
        return jsonify({'status': 'pending'})


if __name__ == '__main__':
    app.run(debug=True)