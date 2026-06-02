from flask import Flask, render_template_string
import subprocess
import sys
import os

app = Flask(__name__)

# HTML template for the mobile trigger page
MOBILE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aadya Inauguration - Mobile Trigger</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
        }
        
        .container {
            text-align: center;
            padding: 20px;
            max-width: 90%;
        }
        
        h1 {
            font-size: 24px;
            color: #00FFFF;
            margin-bottom: 10px;
        }
        
        h2 {
            font-size: 20px;
            color: #FF69B4;
            margin-bottom: 8px;
        }
        
        h3 {
            font-size: 16px;
            color: #FFFF00;
            margin-bottom: 30px;
        }
        
        .launch-btn {
            background: #00FF00;
            color: #000000;
            border: none;
            padding: 30px 60px;
            font-size: 32px;
            font-weight: bold;
            border-radius: 15px;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0, 255, 0, 0.3);
            transition: all 0.3s;
            margin: 20px;
        }
        
        .launch-btn:active {
            transform: scale(0.95);
            box-shadow: 0 4px 10px rgba(0, 255, 0, 0.5);
        }
        
        .status {
            margin-top: 30px;
            font-size: 18px;
            color: #00FF00;
            min-height: 30px;
        }
        
        .note {
            margin-top: 20px;
            font-size: 14px;
            color: #CCCCCC;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Women In Engineering Affinity Group Kssem</h1>
        <h2>Aadya</h2>
        <h3>Inauguration Ceremony</h3>
        
        <button class="launch-btn" onclick="launchVideo()">LAUNCH</button>
        
        <div class="status" id="status">Ready to launch</div>
        <div class="note">Tap the button to trigger the inauguration video</div>
    </div>
    
    <script>
        function launchVideo() {
            const statusEl = document.getElementById('status');
            statusEl.textContent = 'Launching...';
            statusEl.style.color = '#FFFF00';
            
            fetch('/trigger', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusEl.textContent = 'Video Launched Successfully!';
                    statusEl.style.color = '#00FF00';
                } else {
                    statusEl.textContent = 'Error: ' + data.message;
                    statusEl.style.color = '#FF0000';
                }
            })
            .catch(error => {
                statusEl.textContent = 'Failed to connect';
                statusEl.style.color = '#FF0000';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Display the mobile trigger page"""
    return render_template_string(MOBILE_PAGE)

@app.route('/trigger', methods=['POST'])
def trigger():
    """Trigger the inauguration video directly"""
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "import cv2.py")
        
        # Check if the main script exists
        if not os.path.exists(main_script):
            return {'success': False, 'message': f'Script not found: {main_script}'}
        
        # Run the main handshake detection script
        subprocess.Popen([sys.executable, main_script])
        
        return {'success': True, 'message': 'Video launched successfully'}
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

def main():
    import socket
    
    # Get the local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*70)
    print("🌐 MOBILE TRIGGER SERVER STARTED")
    print("="*70)
    print(f"\n📱 Access from your mobile device:")
    print(f"\n   http://{local_ip}:5000")
    print(f"\n   OR")
    print(f"\n   http://localhost:5000 (same computer)")
    print("\n" + "="*70)
    print("\n💡 Make sure your mobile device is on the same WiFi network!")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
