import os
import subprocess
import tempfile
from flask import Flask, render_template, request, Response, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def run_adb_command(command):
    """Runs an ADB command and returns the output."""
    try:
        # command is a list, e.g., ['adb', 'devices']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"ADB Error: {e.stderr}")
        return None
    except FileNotFoundError:
        print("ADB not found. Make sure it is installed and in PATH.")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_device')
def check_device():
    output = run_adb_command(['adb', 'devices'])
    if not output:
        return jsonify({'connected': False, 'message': 'ADB not found or error'})
    
    # Parse output. First line is "List of devices attached".
    # Subsequent lines are "serial\tdevice"
    lines = output.split('\n')
    devices = []
    for line in lines[1:]:
        if line.strip() and '\tdevice' in line:
            devices.append(line.split('\t')[0])
            
    if devices:
        return jsonify({'connected': True, 'devices': devices, 'message': f'Connected: {devices[0]}'})
    else:
        return jsonify({'connected': False, 'message': 'No device found. Enable USB Debugging.'})

@app.route('/list_apps')
def list_apps():
    # List 3rd party packages with their paths
    # Output format: package:/data/app/~~.../base.apk=com.example.app
    output = run_adb_command(['adb', 'shell', 'pm', 'list', 'packages', '-f', '-3'])
    if not output:
        return jsonify({'error': 'Failed to list apps'}), 500
        
    apps = []
    for line in output.split('\n'):
        if line.startswith('package:'):
            # Remove 'package:' prefix
            line = line[8:]
            # Split by '=' to get path and package name
            parts = line.rsplit('=', 1)
            if len(parts) == 2:
                path = parts[0]
                package_id = parts[1]
                apps.append({'id': package_id, 'path': path})
    
    # Sort by package ID
    apps.sort(key=lambda x: x['id'])
    return jsonify({'apps': apps})

@app.route('/download', methods=['POST'])
def download():
    package_path = request.form.get('package_path')
    package_id = request.form.get('package_id')
    
    if not package_path or not package_id:
        return "Missing package info", 400

    # Create a temp directory to pull the APK to
    temp_dir = tempfile.mkdtemp()
    local_filename = f"{package_id}.apk"
    local_path = os.path.join(temp_dir, local_filename)
    
    print(f"Pulling {package_path} to {local_path}...")
    
    # Run adb pull
    try:
        subprocess.run(['adb', 'pull', package_path, local_path], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return f"Failed to pull APK: {e.stderr}", 500

    # Stream the file to the user and then delete it (cleanup is tricky with send_file, 
    # but we can rely on OS cleaning temp eventually or use a generator)
    
    try:
        return send_file(local_path, as_attachment=True, download_name=local_filename)
    except Exception as e:
        return f"Error sending file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
