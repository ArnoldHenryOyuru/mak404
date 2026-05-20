import qrcode
import sys

# Replace with your deployed URL
url = sys.argv[1] if len(sys.argv) > 1 else "https://your-app.onrender.com?sN=2500731619&cat=reg_details"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save('qr_final.png')
print(f"QR generated for: {url}")
