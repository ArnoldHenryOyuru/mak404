from flask import Flask, render_template_string, abort, request
import os

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>DOCUMENT VERIFICATION PORTAL</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
  <style>
    *,*:before,*:after{box-sizing:border-box;margin:0;padding:0}
    html,body{min-height:100vh;font-family:'Poppins',sans-serif;font-size:14px;background:#67697414;color:#212529}
    body{background-color:#f0f0f0 !important;background-image:none;}
    .page-wrapper{min-height:100vh;display:flex;flex-direction:column;}
    /* NAVBAR */
    .navbar{background:#23a74c;padding:0;}
    /* MAIN */
    .main{flex:1;padding:40px 60px;}
    .layout{display:grid;grid-template-columns:1fr 1fr;gap:40px;max-width:1100px;margin:0 auto;}
    /* LEFT */
    .left-logo{display:flex;flex-direction:column;align-items:center;margin-bottom:12px;}
    .left-logo img{width:180px;}
    .left-logo .uni-name{color:#23a74c;font-weight:700;font-size:15px;letter-spacing:.5px;text-align:center;margin-top:8px;}
    .left-logo .portal-title{color:#23a74c;font-weight:700;font-size:13px;letter-spacing:.5px;text-align:center;}
    .doc-types-title{color:#23a74c;font-weight:800;font-size:16px;letter-spacing:.5px;margin:16px 0 12px;text-transform:uppercase;}
    .doc-list{list-style:none;display:flex;flex-direction:column;gap:14px;}
    .doc-item{display:flex;align-items:center;gap:14px;color:#23a74c;font-weight:700;font-size:13px;letter-spacing:.5px;text-transform:uppercase;}
    .doc-item svg{width:36px;height:36px;flex-shrink:0;stroke:#23a74c;fill:none;stroke-width:1.5;}
    /* RIGHT */
    .right{display:flex;flex-direction:column;align-items:center;padding-top:20px;}
    .qr-icon{margin-bottom:16px;}
    .qr-icon svg{width:90px;height:90px;stroke:#23a74c;fill:none;stroke-width:2.5;}
    .scan-text{font-weight:700;font-size:13px;text-align:center;max-width:280px;letter-spacing:.3px;margin-bottom:24px;}
    .doc-preview{position:relative;width:200px;height:130px;margin-bottom:8px;}
    .doc-card{position:absolute;background:white;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:10px;display:flex;gap:8px;align-items:flex-start;}
    .doc-card.back{width:160px;height:110px;left:40px;top:0;z-index:1;}
    .doc-card.front{width:160px;height:110px;left:0px;top:15px;z-index:2;}
    .avatar{width:36px;height:36px;background:#ccc;border-radius:50%;flex-shrink:0;}
    .lines{flex:1;display:flex;flex-direction:column;gap:5px;padding-top:4px;}
    .line{height:6px;background:#e0e0e0;border-radius:3px;}
    .line.short{width:60%;}
    .checkmark{position:absolute;bottom:6px;right:8px;z-index:3;background:#23a74c;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;}
    .checkmark svg{width:16px;height:16px;stroke:white;fill:none;stroke-width:3;}
    /* inbox icon */
    .inbox-icon{margin-top:30px;margin-bottom:10px;}
    .inbox-icon svg{width:80px;height:70px;}
    .no-qr{color:#bd3128;font-weight:800;font-size:13px;letter-spacing:.5px;text-transform:uppercase;margin-bottom:16px;}
    .btn-student{background:#23a74c;color:white;border:3px solid #1a8a3c;border-radius:8px;padding:14px 32px;font-family:'Poppins',sans-serif;font-weight:700;font-size:13px;letter-spacing:.5px;cursor:pointer;text-transform:uppercase;}
    /* FOOTER */
    .footer{background:#23a74c;color:white;text-align:center;padding:16px;font-weight:700;font-size:13px;letter-spacing:.3px;}
    /* Loading overlay */
    .loading-overlay{display:none;position:fixed;inset:0;background:rgba(240,240,240,.95);z-index:999;flex-direction:column;align-items:center;justify-content:center;gap:20px;}
    .loading-overlay.active{display:flex;}
    .spinner{width:48px;height:48px;border:5px solid #e0e0e0;border-top-color:#23a74c;border-radius:50%;animation:spin .9s linear infinite;}
    @keyframes spin{to{transform:rotate(360deg)}}
    .loading-status{font-size:14px;color:#555;font-family:'Poppins',sans-serif;}
    .loading-bar-wrap{width:260px;height:5px;background:#e0e0e0;border-radius:3px;overflow:hidden;}
    .loading-bar{height:100%;width:0%;background:#23a74c;border-radius:3px;transition:width .4s ease;}
    .loading-title{font-family:'Poppins',sans-serif;font-weight:700;color:#23a74c;font-size:15px;letter-spacing:.5px;}
  </style>
</head>
<body>
<!-- Loading overlay -->
<div class="loading-overlay" id="loader">
  <div class="loading-title">MAKERERE UNIVERSITY</div>
  <div style="font-size:12px;color:#888;margin-top:-12px;">Document Verification Portal</div>
  <div class="spinner"></div>
  <div class="loading-status" id="load-status">Connecting to server...</div>
  <div class="loading-bar-wrap"><div class="loading-bar" id="load-bar"></div></div>
</div>

<div class="page-wrapper">
  <div class="main">
    <div class="layout">
      <!-- LEFT -->
      <div>
        <div class="left-logo">
          <img src="https://documents.mak.ac.ug/static/media/undraw_hiring_re_yk5n.55733c22e8e8959ad7cb.svg" onerror="this.style.display='none'" alt=""/>
          <!-- Mak coat of arms SVG fallback -->
          <div style="width:160px;height:160px;background:#f5f5f5;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;color:#23a74c;font-size:32px;margin-bottom:8px;">MU</div>
          <div class="uni-name">MAKERERE UNIVERSITY</div>
          <div class="portal-title">DOCUMENT VERIFICATION PORTAL</div>
        </div>
        <div class="doc-types-title">TYPES OF DOCUMENTS</div>
        <ul class="doc-list">
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><rect x="4" y="2" width="14" height="18" rx="2"/><polyline points="8,8 16,8"/><polyline points="8,12 16,12"/><path d="M15,18l2,2 4-4"/></svg>
            PROOF OF REGISTRATION
          </li>
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><rect x="4" y="2" width="14" height="18" rx="2"/><path d="M9,12l2,2 4-4"/><polyline points="8,7 16,7"/></svg>
            EXAMINATION PERMIT
          </li>
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            CERTIFICATE
          </li>
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><rect x="4" y="2" width="14" height="18" rx="2"/><polyline points="8,7 16,7"/><polyline points="8,11 16,11"/><polyline points="8,15 12,15"/><path d="M14,18l2,2 4-4"/></svg>
            TRANSCRIPT
          </li>
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><rect x="4" y="14" width="16" height="7" rx="2"/><line x1="9" y1="14" x2="9" y2="21"/><line x1="15" y1="14" x2="15" y2="21"/></svg>
            VIRTUAL ID
          </li>
          <li class="doc-item">
            <svg viewBox="0 0 24 24"><rect x="4" y="2" width="14" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><polyline points="13,7 17,7"/><polyline points="13,11 17,11"/><polyline points="8,15 16,15"/></svg>
            GRADUATION INVITATION CARD
          </li>
        </ul>
      </div>
      <!-- RIGHT -->
      <div class="right">
        <!-- QR Icon -->
        <div class="qr-icon">
          <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:90px;height:90px;">
            <rect x="5" y="5" width="38" height="38" rx="4" fill="none" stroke="#23a74c" stroke-width="5"/>
            <rect x="15" y="15" width="18" height="18" fill="#23a74c"/>
            <rect x="57" y="5" width="38" height="38" rx="4" fill="none" stroke="#23a74c" stroke-width="5"/>
            <rect x="67" y="15" width="18" height="18" fill="#23a74c"/>
            <rect x="5" y="57" width="38" height="38" rx="4" fill="none" stroke="#23a74c" stroke-width="5"/>
            <rect x="15" y="67" width="18" height="18" fill="#23a74c"/>
            <rect x="57" y="57" width="10" height="10" fill="#23a74c"/>
            <rect x="72" y="57" width="10" height="10" fill="#23a74c"/>
            <rect x="57" y="72" width="10" height="10" fill="#23a74c"/>
            <rect x="87" y="72" width="10" height="10" fill="#23a74c"/>
            <rect x="72" y="87" width="10" height="10" fill="#23a74c"/>
            <rect x="87" y="57" width="10" height="10" fill="#23a74c"/>
          </svg>
        </div>
        <div class="scan-text">SCAN THE QR CODE ON YOUR DOCUMENT TO VERIFY.</div>
        <!-- Doc preview cards -->
        <div style="position:relative;width:220px;height:150px;margin-bottom:12px;">
          <div style="position:absolute;background:white;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:10px;width:155px;height:105px;left:55px;top:0;z-index:1;display:flex;gap:8px;">
            <div style="width:34px;height:34px;background:#ddd;border-radius:50%;flex-shrink:0;"></div>
            <div style="flex:1;display:flex;flex-direction:column;gap:5px;padding-top:2px;">
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:100%;"></div>
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:80%;"></div>
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:60%;"></div>
            </div>
          </div>
          <div style="position:absolute;background:white;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.2);padding:10px;width:155px;height:105px;left:10px;top:20px;z-index:2;display:flex;gap:8px;">
            <div style="width:34px;height:34px;background:#ddd;border-radius:50%;flex-shrink:0;"></div>
            <div style="flex:1;display:flex;flex-direction:column;gap:5px;padding-top:2px;">
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:100%;"></div>
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:70%;"></div>
              <div style="height:6px;background:#e0e0e0;border-radius:3px;width:50%;"></div>
            </div>
          </div>
          <div style="position:absolute;bottom:6px;right:44px;z-index:3;background:#23a74c;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;">
            <svg viewBox="0 0 24 24" style="width:16px;height:16px;stroke:white;fill:none;stroke-width:3;"><polyline points="4,12 9,17 20,6"/></svg>
          </div>
        </div>
        <!-- Inbox icon -->
        <div style="margin:16px 0 8px;">
          <svg viewBox="0 0 100 80" style="width:85px;height:70px;" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 20 L50 50 L90 20" stroke="#c5d8f0" stroke-width="3" fill="none"/>
            <rect x="5" y="18" width="90" height="55" rx="6" fill="#5b9bd5" opacity=".7"/>
            <rect x="5" y="18" width="90" height="20" rx="6" fill="#4a8bc4" opacity=".8"/>
            <path d="M5 38 L5 73 Q5 73 5 73 L95 73 L95 38 L60 56 Q50 62 40 56 Z" fill="#6aaee0" opacity=".9"/>
          </svg>
        </div>
        <div class="no-qr">NO QR CODE SCAN DETECTED</div>
        <button class="btn-student" onclick="startLoading()">USE STUDENT NUMBER</button>
      </div>
    </div>
  </div>
  <div class="footer">©2026 – HEMIS Consortium. All rights Reserved.</div>
</div>

<script>
const steps = [
  [700,  "Authenticating request...",       15],
  [1600, "Fetching registration record...", 40],
  [2600, "Verifying student number...",     70],
  [3400, "Loading document...",             90],
  [4200, "Almost there...",                 99],
];

function runCycle() {
  const bar = document.getElementById('load-bar');
  const status = document.getElementById('load-status');
  bar.style.transition = 'none';
  bar.style.width = '0%';
  status.textContent = 'Connecting to server...';
  setTimeout(() => {
    bar.style.transition = 'width .4s ease';
    steps.forEach(([delay, msg, pct]) => {
      setTimeout(() => { status.textContent = msg; bar.style.width = pct + '%'; }, delay);
    });
    setTimeout(runCycle, 5000);
  }, 80);
}

function startLoading() {
  document.getElementById('loader').classList.add('active');
  runCycle();
}
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML), 200

@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)