from flask import Flask, abort, request, render_template_string
import os

app = Flask(__name__)

LOADING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Makerere University — Documents Portal</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #f4f4f4;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      color: #333;
    }
    .card {
      background: white;
      border-radius: 8px;
      padding: 48px 40px;
      text-align: center;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
      max-width: 400px;
      width: 90%;
    }
    .logo {
      width: 72px;
      height: 72px;
      margin: 0 auto 20px;
      background: #1a3c6e;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .logo span { color: white; font-size: 22px; font-weight: 700; }
    h2 { font-size: 17px; color: #1a3c6e; margin-bottom: 6px; }
    p.sub { font-size: 13px; color: #888; margin-bottom: 32px; }
    .spinner {
      width: 44px;
      height: 44px;
      border: 4px solid #e0e0e0;
      border-top-color: #1a3c6e;
      border-radius: 50%;
      animation: spin 0.9s linear infinite;
      margin: 0 auto 20px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .status { font-size: 13px; color: #555; min-height: 20px; }
    .bar-wrap {
      background: #e8e8e8;
      border-radius: 4px;
      height: 4px;
      width: 100%;
      margin: 20px 0 0;
      overflow: hidden;
    }
    .bar {
      height: 100%;
      width: 0%;
      background: #1a3c6e;
      border-radius: 4px;
      transition: width 0.4s ease;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo"><span>MU</span></div>
    <h2>Makerere University</h2>
    <p class="sub">Documents Portal — Fetching your record</p>
    <div class="spinner"></div>
    <div class="status" id="status">Connecting to server...</div>
    <div class="bar-wrap"><div class="bar" id="bar"></div></div>
  </div>

  <script>
    const steps = [
      [600,  "Authenticating request...",      15],
      [1400, "Fetching registration record...", 40],
      [2400, "Verifying student number...",     70],
      [3200, "Loading document...",             90],
      [4000, "Almost there...",                 99],
    ];

    function runCycle() {
      const bar = document.getElementById('bar');
      const status = document.getElementById('status');

      bar.style.transition = 'none';
      bar.style.width = '0%';
      status.textContent = 'Connecting to server...';

      setTimeout(() => {
        bar.style.transition = 'width 0.4s ease';
        steps.forEach(([delay, msg, pct]) => {
          setTimeout(() => {
            status.textContent = msg;
            bar.style.width = pct + '%';
          }, delay);
        });
        setTimeout(runCycle, 4800);
      }, 100);
    }

    runCycle();
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(LOADING_HTML), 200

@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)