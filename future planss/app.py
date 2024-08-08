from flask import Flask, request, send_file, jsonify
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    data = pd.read_excel(file)
    
    images = []
    for index, row in data.iterrows():
        img = Image.new('RGB', (500, 300), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"Name: {row['Name']}", fill=(255, 255, 0))
        d.text((10, 50), f"Info1: {row['Info1']}", fill=(255, 255, 0))
        d.text((10, 90), f"Info2: {row['Info2']}", fill=(255, 255, 0))
        
        image_io = io.BytesIO()
        img.save(image_io, 'PNG')
        image_io.seek(0)
        images.append(image_io)
    
    pdf_io = io.BytesIO()
    c = canvas.Canvas(pdf_io, pagesize=letter)
    
    for image_io in images:
        img = Image.open(image_io)
        c.drawInlineImage(img, 0, 0, width=letter[0], height=letter[1])
        c.showPage()
    
    c.save()
    pdf_io.seek(0)
    
    return send_file(pdf_io, as_attachment=True, download_name='output.pdf')

if __name__ == '__main__':
    app.run(debug=True)
