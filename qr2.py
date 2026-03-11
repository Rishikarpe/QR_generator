import qrcode

# 1. Initialize the QR Code generator
qr = qrcode.QRCode(
  version=1,                           # Simplest version (21x21 modules)
 error_correction=qrcode.constants.ERROR_CORRECT_L, # Lowest error correction (7%)
  box_size=4,                          # Each module will be 4x4 pixels
   border=2,                            # Minimum white border (Quiet Zone)
)

# 2. Add the simplest data (a short string)
data = "A00003,25,120,NATURAL,121,800" 
qr.add_data(data)
qr.make(fit=True)

# 3. Create the image
# This will result in an image roughly 100x100 pixels
img = qr.make_image(fill_color="black", back_color="white")

# 4. Save the file
img.save("simplest_qr.png")
print("QR Code generated as simplest_qr.png")