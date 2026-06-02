from flask import Flask, render_template_string
import subprocess
import sys
import os
import qrcode
import socket

app = Flask(__name__)

# Simple mobile-optimized HTML page
MOBILE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>WIE Aadya Launch</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
            overflow: hidden;
        }
        
        .container {
            text-align: center;
            padding: 20px;
            width: 100%;
            max-width: 500px;
        }
        
        h1 {
            font-size: clamp(18px, 5vw, 28px);
            color: #00FFFF;
            margin-bottom: 8px;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        
        h2 {
            font-size: clamp(16px, 4vw, 22px);
            color: #FF69B4;
            margin-bottom: 6px;
            text-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
        }
        
        h3 {
            font-size: clamp(14px, 3.5vw, 18px);
            color: #FFFF00;
            margin-bottom: 40px;
            text-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
        }
        
        .launch-btn {
            background: linear-gradient(135deg, #00FF00, #00CC00);
            color: #000000;
            border: none;
            padding: 40px 80px;
            font-size: clamp(28px, 8vw, 48px);
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(0, 255, 0, 0.4);
            transition: all 0.2s;
            margin: 30px 0;
            width: 90%;
            max-width: 400px;
            touch-action: manipulation;
        }
        
        .launch-btn:active {
            transform: scale(0.95);
            box-shadow: 0 5px 15px rgba(0, 255, 0, 0.6);
        }
        
        .launch-btn.launching {
            background: linear-gradient(135deg, #FFFF00, #FFA500);
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .status {
            margin-top: 30px;
            font-size: clamp(16px, 4vw, 22px);
            color: #00FF00;
            min-height: 30px;
            text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
        }
        
        .status.error {
            color: #FF0000;
            text-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
        }
        
        .icon {
            font-size: 60px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🎬</div>
        <h1>Women In Engineering<br>Affinity Group Kssem</h1>
        <h2>Aadya</h2>
        <h3>Inauguration Ceremony</h3>
        
        <button class="launch-btn" id="launchBtn" onclick="launchVideo()">
            LAUNCH
        </button>
        
        <div class="status" id="status">📱 Tap to Launch</div>
    </div>
    
    <script>
        let launching = false;
        
        function launchVideo() {
            if (launching) return;
            
            launching = true;
            const btn = document.getElementById('launchBtn');
            const statusEl = document.getElementById('status');
            
            btn.classList.add('launching');
            btn.textContent = '⏳';
            statusEl.textContent = '🚀 Launching...';
            statusEl.style.color = '#FFFF00';
            
            fetch('/launch', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusEl.textContent = '✅ Video Launched!';
                    statusEl.style.color = '#00FF00';
                    btn.textContent = '✓';
                    setTimeout(() => {
                        btn.classList.remove('launching');
                        btn.textContent = 'LAUNCH';
                        statusEl.textContent = '📱 Tap to Launch';
                        launching = false;
                    }, 3000);
                } else {
                    statusEl.textContent = '❌ Error: ' + data.message;
                    statusEl.classList.add('error');
                    btn.classList.remove('launching');
                    btn.textContent = 'LAUNCH';
                    launching = false;
                }
            })
            .catch(error => {
                statusEl.textContent = '❌ Connection Failed';
                statusEl.classList.add('error');
                btn.classList.remove('launching');
                btn.textContent = 'LAUNCH';
                launching = false;
            });
        }
        
        // Prevent double-tap zoom
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Display the mobile launch page"""
    return render_template_string(MOBILE_PAGE)

@app.route('/launch', methods=['POST'])
def launch():
    """Launch the inauguration video"""
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "import cv2.py")
        
        # Check if the main script exists
        if not os.path.exists(main_script):
            return {'success': False, 'message': f'Script not found'}
        
        # Run the main handshake detection script
        subprocess.Popen([sys.executable, main_script])
        
        return {'success': True, 'message': 'Video launched successfully'}
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

def generate_qr_code(url):
    """Generate QR code for the URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(os.path.dirname(__file__), "mobile_launch_qr.png")
    img.save(qr_path)
    return qr_path

def main():
    # Get the local IP address
    hostname = socket.gethostname()
    try:
        # Try to get actual network IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = socket.gethostbyname(hostname)
    
    # Create the URL
    url = f"http://{local_ip}:8080"
    
    # Generate QR code
    qr_path = generate_qr_code(url)
    
    print("\n" + "="*80)
    print("📱 MOBILE LAUNCH SERVER - WIE AADYA INAUGURATION")
    print("="*80)
    print(f"\n🌐 Mobile Access URL:")
    print(f"\n   {url}")
    print(f"\n📷 QR Code saved to: {qr_path}")
    print(f"\n   Scan the QR code with your phone's camera app!")
    print("\n" + "="*80)
    print("\n💡 Instructions:")
    print("   1. Make sure your phone is on the same WiFi network")
    print("   2. Open the QR code image and scan it with your phone")
    print("   3. OR manually type the URL in your phone's browser")
    print("   4. Tap the green LAUNCH button to trigger the video")
    print("\n⚠️  IMPORTANT - If link doesn't work:")
    print("   • Allow Python through Windows Firewall")
    print("   • Make sure phone and PC are on SAME WiFi")
    print("   • Check if you can ping this computer from phone")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("\n" + "="*80 + "\n")
    
    # Open QR code in default image viewer
    try:
        if os.name == 'nt':  # Windows
            os.startfile(qr_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(['open', qr_path])
    except:
        pass
    
    print("🟢 Server starting...\n")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

if __name__ == '__main__':
    main()
