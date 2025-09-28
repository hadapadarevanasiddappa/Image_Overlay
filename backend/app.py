from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io, os
from rembg import remove
import traceback

app = Flask(__name__)

# List of font file names placed inside static/fonts directory
FONTS = [
    "arial.ttf",
    "calibri.ttf",
    "algerian.ttf",
    "poppins.ttf",
    "Roboto-Regular.ttf",
    "RobotoCondensed-Regular.ttf",
    "RobotoSlab-Regular.ttf",
    "LibreFranklin-Regular.ttf",
    "Raleway-Regular.ttf",
    "Inter-Regular.ttf",
    "SourceSansPro-Regular.ttf",
    "Poppins-Regular.ttf",
    "DMSans-Regular.ttf",
    "PlayfairDisplay-Regular.ttf",
    "Rubik-Regular.ttf",
    "Lora-Regular.ttf"
]

@app.context_processor
def inject_theme():
    return dict()

@app.route('/')
def index():
    return render_template('index.html', fonts=FONTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        file = request.files['image']
        text = request.form['custom_text']
        font_style = request.form['font_style']
        text_color = request.form['text_color']
        font_scale = int(request.form['font_scale'])

        # Open image
        img = Image.open(file).convert("RGBA")

        # Remove background
        subject = remove(img).convert("RGBA")

        # Glow effect for subject
        glow = subject.filter(ImageFilter.GaussianBlur(radius=30))

        # Create text layer
        text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        # Load font
        font_path = os.path.join("static", "fonts", font_style)
        font_size = int((font_scale / 100) * img.height)
        font = ImageFont.truetype(font_path, size=font_size)

        # Text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2

        # Draw glowing background text
        glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        for offset in range(1, 6):
            glow_draw.text((x - offset, y), text, font=font, fill=text_color)
            glow_draw.text((x + offset, y), text, font=font, fill=text_color)
            glow_draw.text((x, y - offset), text, font=font, fill=text_color)
            glow_draw.text((x, y + offset), text, font=font, fill=text_color)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))

        # Draw actual text
        draw.text((x, y), text, font=font, fill=text_color)

        # Composite: background -> glow -> text -> subject
        combined = Image.alpha_composite(img, glow_layer)
        combined = Image.alpha_composite(combined, text_layer)
        combined = Image.alpha_composite(combined, glow)
        combined = Image.alpha_composite(combined, subject)

        # Convert to RGB and return
        output = combined.convert("RGB")
        buf = io.BytesIO()
        output.save(buf, format="JPEG")
        buf.seek(0)

        return send_file(buf, mimetype='image/jpeg')

    except Exception as e:
        traceback.print_exc()  # For debugging in terminal
        return f"Image processing failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
