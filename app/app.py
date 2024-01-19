from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploader', methods=['POST'])
def upload_file_and_process():
    if request.method == 'POST':
        excel = request.files['excel']
        template = request.files['template']
        output_path = request.form['output_path']

        # Save the uploaded files temporarily
        excel_path = os.path.join('uploads', excel.filename)
        template_path = os.path.join('uploads', template.filename)

        excel.save(excel_path)
        template.save(template_path)

        # Process the script using the uploaded files
        process_image(excel_path, template_path, output_path)

        # After processing, send the edited image to the user
        return send_file(output_path, as_attachment=True)

def process_image(excel_path, template_image_path, edited_image_path):
    # Load the Excel file to read the data
    names_df = pd.read_excel(excel_path)

    # Extract the names and coordinates
    column_h_names = names_df['Convocados'].tolist()
    column_i_names = names_df['Dorsales'].tolist()
    x1_coords = names_df['X1'].tolist()
    x2_coords = names_df['X2'].tolist()
    y_coords = names_df['Y'].tolist()

    # Load the template image
    template_image = Image.open(template_image_path)
    draw = ImageDraw.Draw(template_image)

    # Define fonts (update the font paths as needed)
    
    font_path_regular = os.path.join('static', 'fonts', 'OldSport01CollegeNcv-aeGm.ttf')
    font_path_large = os.path.join('static', 'fonts', 'OldSport01CollegeNcv-aeGm.ttf')
    font_path_equipos = os.path.join('static', 'fonts', 'THE BOLD FONT - FREE VERSION - 2023.ttf')

    font_regular = ImageFont.truetype(font_path_regular, size=28)
    font_large = ImageFont.truetype(font_path_large, size=38)
    font_equipos = ImageFont.truetype(font_path_equipos, size=24)

    # Function to draw text on the image
    def draw_text(draw, names, x_coords, y_coords, font, fill):
        for name, x, y in zip(names, x_coords, y_coords):
            if pd.notna(name) and pd.notna(x) and pd.notna(y):
                position = (int(x), int(y))
                draw.text(position, str(name), font=font, fill=fill)

    # Draw the names
    draw_text(draw, column_h_names, x1_coords, y_coords, font_large, "black")
    draw_text(draw, column_i_names, x2_coords, y_coords, font_regular, "white")

    # Save the edited image
    template_image.save(edited_image_path)

if __name__ == '__main__':
    app.run(debug=True)
