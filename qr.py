import io
import os
import qrcode
from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "dbspackaging_logo.jpg")

app = Flask(__name__)


@app.route("/logo")
def logo():
    return send_file(LOGO_PATH, mimetype="image/jpeg")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    reel   = request.form["reel"].strip()
    bf     = request.form["bf"].strip()
    gsm    = request.form["gsm"].strip()
    shade  = request.form["shade"].strip()
    size   = request.form["size"].strip()
    weight = request.form["weight"].strip()

    data = f"{reel},{bf},{gsm},{shade},{size},{weight}"

    # --- QR code -> in-memory PNG ---
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)

    # --- PDF -> in-memory ---
    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=A4)
    page_w, page_h = A4
    label_h = 12 * mm

    from reportlab.lib.utils import ImageReader

    # --- Logo at top of PDF ---
    logo_h = 20 * mm
    logo_w = 60 * mm
    c.drawImage(
        LOGO_PATH,
        (page_w - logo_w) / 2, page_h - logo_h - 4 * mm,
        width=logo_w, height=logo_h,
        preserveAspectRatio=True, mask="auto",
    )

    # QR shifted down to make room for logo
    qr_size = min(page_w, page_h - logo_h - label_h - 8 * mm)
    x = (page_w - qr_size) / 2
    y = page_h - logo_h - 8 * mm - qr_size

    c.drawImage(ImageReader(qr_buf), x, y, width=qr_size, height=qr_size)
    c.setFont("Helvetica-Bold", 35)
    c.drawCentredString(page_w / 2, y - 10 * mm, reel)
    c.save()
    pdf_buf.seek(0)

    return send_file(
        pdf_buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{reel}.pdf",
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000)
