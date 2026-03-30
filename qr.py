import qrcode

# Data you want inside QR
data = "http://127.0.0.1:8000/order/abc123/"

# Generate QR
qr = qrcode.make(data)

# Save image
qr.save("test_qr.png")

print("QR generated successfully")