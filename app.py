import qrcode
from flask import Flask, request, redirect
import os

# ============================================
# CONFIGURATION - UPDATE THESE URLs
# ============================================
IOS_APP_URL = "https://apps.apple.com/np/app/veel-app/id6455370559"
ANDROID_APP_URL = "https://play.google.com/store/apps/details?id=com.veel.app&hl=en"
FALLBACK_URL = "https://veelapp.com/?tab=creators"

# Flask app for handling redirects
app = Flask(__name__)

@app.route('/')
def home():
    """Home page with instructions and QR code"""
    qr_url = request.host_url + 'app'
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Veel App - Smart Redirect</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .subtitle {{
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }}
            .button {{
                display: inline-block;
                margin: 10px;
                padding: 15px 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-size: 18px;
                font-weight: 600;
                transition: transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }}
            .button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            .qr-container {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
            }}
            #qrCanvas {{
                display: inline-block;
                padding: 15px;
                background: white;
                border-radius: 10px;
            }}
            .features {{
                margin-top: 30px;
                text-align: left;
                color: #555;
            }}
            .feature {{
                margin: 15px 0;
                padding-left: 30px;
                position: relative;
            }}
            .feature:before {{
                content: "✓";
                position: absolute;
                left: 0;
                color: #667eea;
                font-weight: bold;
                font-size: 1.2em;
            }}
            .qr-label {{
                color: #666;
                font-size: 0.95em;
                margin-bottom: 15px;
            }}
            @media (max-width: 600px) {{
                .container {{ padding: 20px; }}
                h1 {{ font-size: 1.8em; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Veel App</h1>
            <p class="subtitle">Download our app for the best experience!</p>
            
            <div class="qr-container">
                <p class="qr-label">Scan with your phone:</p>
                <div id="qrCanvas"></div>
            </div>
            
            <a href="/app" class="button">Download Now</a>
            <a href="/qr" class="button">View QR & Link</a>
            
            <div class="features">
                <div class="feature">Automatically detects your device</div>
                <div class="feature">Redirects to the right app store</div>
                <div class="feature">Works on iOS, Android & Desktop</div>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
        <script>
            // Generate QR code
            new QRCode(document.getElementById("qrCanvas"), {{
                text: "{qr_url}",
                width: 256,
                height: 256,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            }});
        </script>
    </body>
    </html>
    """

@app.route('/app')
def smart_redirect():
    """Detect device and redirect accordingly"""
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Log for debugging
    app.logger.info(f"User-Agent: {user_agent}")
    app.logger.info(f"IP Address: {request.remote_addr}")
    
    # Detect iOS devices
    if any(device in user_agent for device in ['iphone', 'ipad', 'ipod']):
        app.logger.info("Redirecting to iOS App Store")
        return redirect(IOS_APP_URL)
    
    # Detect Android devices
    elif 'android' in user_agent:
        app.logger.info("Redirecting to Google Play Store")
        return redirect(ANDROID_APP_URL)
    
    # Fallback for other devices (desktop, etc.)
    else:
        app.logger.info("Redirecting to fallback URL")
        return redirect(FALLBACK_URL)

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return {'status': 'healthy', 'service': 'Veel App Smart Redirect'}, 200

@app.route('/qr')
def show_qr():
    """Page to display and download QR code"""
    qr_url = request.host_url + 'app'
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Veel App - QR Code & Link</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                margin: 40px auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2em;
            }}
            .qr-container {{
                background: #f8f9fa;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
            }}
            #qrCanvas {{
                display: inline-block;
                padding: 20px;
                background: white;
                border-radius: 10px;
            }}
            .link-section {{
                margin: 30px 0;
            }}
            .link-section h3 {{
                color: #555;
                margin-bottom: 15px;
                text-align: center;
            }}
            .link-box {{
                background: #f8f9fa;
                padding: 20px;
                border: 2px solid #667eea;
                border-radius: 10px;
                word-break: break-all;
                font-family: monospace;
                font-size: 14px;
                text-align: center;
                color: #333;
            }}
            .button-group {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                margin-top: 20px;
            }}
            .btn {{
                padding: 12px 25px;
                border: none;
                border-radius: 50px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                text-decoration: none;
                display: inline-block;
            }}
            .btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }}
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            .btn-success {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
            }}
            .btn-success:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(17, 153, 142, 0.6);
            }}
            .info-box {{
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .info-box p {{
                color: #555;
                line-height: 1.6;
                margin: 5px 0;
            }}
            @media (max-width: 600px) {{
                .container {{ padding: 20px; }}
                h1 {{ font-size: 1.5em; }}
                .btn {{ padding: 10px 20px; font-size: 14px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Veel App - QR Code & Link</h1>
            
            <div class="qr-container">
                <h3 style="color: #555; margin-bottom: 20px;">Scan this QR Code:</h3>
                <div id="qrCanvas"></div>
            </div>
            
            <div class="link-section">
                <h3>Or share this link:</h3>
                <div class="link-box" id="linkBox">{qr_url}</div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-success" onclick="copyLink()">📋 Copy Link</button>
                <button class="btn btn-primary" onclick="downloadQR()">⬇️ Download QR</button>
                <a href="/app" class="btn btn-primary">🧪 Test Redirect</a>
            </div>
            
            <div class="info-box">
                <p><strong>📱 How it works:</strong></p>
                <p>✓ iPhone/iPad → Redirects to App Store</p>
                <p>✓ Android → Redirects to Play Store</p>
                <p>✓ Desktop → Redirects to Website</p>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
        <script>
            // Generate QR code
            new QRCode(document.getElementById("qrCanvas"), {{
                text: "{qr_url}",
                width: 256,
                height: 256,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            }});
            
            // Copy link function
            function copyLink() {{
                const link = document.getElementById('linkBox').textContent.trim();
                navigator.clipboard.writeText(link).then(() => {{
                    alert('✓ Link copied to clipboard!');
                }}).catch(err => {{
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = link;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    alert('✓ Link copied to clipboard!');
                }});
            }}
            
            // Download QR code function
            function downloadQR() {{
                const canvas = document.querySelector('#qrCanvas canvas');
                const link = document.createElement('a');
                link.download = 'veel_app_qr_code.png';
                link.href = canvas.toDataURL();
                link.click();
                alert('✓ QR code downloaded!');
            }}
        </script>
    </body>
    </html>
    """

# For production deployment with Gunicorn
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)