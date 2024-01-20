from flask import Flask, request, jsonify,session, send_file
import pandas as pd
from flask import Flask, render_template
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'your_complex_secret_key'  # Replace this with your generated key



@app.route('/')
def home():
    return render_template('index.html')  # Assuming you have an 'index.html' template


@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    excel = request.files['file']
    excel_path = os.path.join('uploads', excel.filename)
    excel.save(excel_path)

    # Assuming the player names are in the first column and numbers in the second
    players_df = pd.read_excel(excel_path, usecols=[0, 1])
    players_df['Number'] = players_df['Number'].astype(str)  # Convert numbers to strings if needed
    players = players_df.to_dict(orient='records')
    # Convert any non-standard types to standard types here
    for player in players:
        for key, value in player.items():
            if isinstance(value, np.integer):
                player[key] = int(value)  # Convert numpy integers to Python integers
            elif isinstance(value, np.floating):
                player[key] = float(value)  # Convert numpy floats to Python floats
            elif isinstance(value, np.ndarray):
                player[key] = value.tolist()  # Convert arrays to lists
            # Add more conversions as necessary
    session['players'] = players
    return jsonify(players)

def process_image(selected_players, template_image_path, coach, date, teams):
    # Load the template image
    template_image = Image.open(template_image_path)
    draw = ImageDraw.Draw(template_image)

    # Define the fonts (update the font paths as needed)
    font_path_regular = os.path.join('static', 'fonts', 'BebasNeue-Regular.ttf')
    font_path_large = os.path.join('static', 'fonts', 'BebasNeue-Regular.ttf')
    font_regular = ImageFont.truetype(font_path_regular, size=35)
    font_large = ImageFont.truetype(font_path_large, size=35)
    font_coach = ImageFont.truetype(font_path_large, size= 45)

    # Coordinates for each player (x for number, x for name, y for both)
    coordinates = [
    (500, 540, 400),
    (500, 540, 440),
    (500, 540, 480),
    (500, 540, 520),
    (500, 540, 560),
    (500, 540, 600),
    (500, 540, 640),
    (500, 540, 680),
    (500, 540, 720),
    (735, 775, 400),
    (735, 775, 440),
    (735, 775, 480),
    (735, 775, 520),
    (735, 775, 560),
    (735, 775, 600),
    (735, 775, 640),
    (735, 775, 680),
    (735, 775, 720)]
    
     # Define coordinates for coach and date
    coach_coords = (500, 800)  # Replace with actual coordinates
    date_coords = (670, 210)     # Replace with actual coordinates
    teams_coords = (670, 250)     # Replace with actual coordinates
    
    # Draw the coach name and date
    draw.text(coach_coords, coach, font=font_coach, fill="#052C54")
    draw.text(date_coords, date, font=font_regular, fill="#052C54")
    draw.text(teams_coords, teams, font=font_regular, fill="#052C54")

    # Ensure we don't try to print more players than there are coordinates
    for index, player in enumerate(selected_players):
            if index < len(coordinates):
                x_number,x_name, y = coordinates[index]
                name = player['name']
                number = player['number']

                # Draw the player number at its X coordinate and shared Y coordinate
                draw.text((x_number, y), str(number), font=font_regular, fill="#052C54",align="left")

                # Draw the player name at its X coordinate and shared Y coordinate
                draw.text((x_name, y), name, font=font_large, fill="white")

    # Save the edited image
        # Save the image to a BytesIO object
    img_byte_arr = BytesIO()
    template_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Go to the start of the BytesIO object

    return img_byte_arr




@app.route('/build-convo', methods=['POST'])
def build_convo():
    data = request.json
    selected_players = data['selected_players']
    template_image_path = session.get('template_path')  # Get the path from the session
    coach = data['coach']
    date = data['date']
    teams = data['teams']

    image_io = process_image(selected_players, template_image_path,coach,date,teams)

    return send_file(image_io, mimetype='image/png', download_name='convo.png', as_attachment=True)


    

@app.route('/get-players', methods=['GET'])
def get_players():
    # Load the players from the stored Excel file or database
    # For example, if you saved the players in a global variable:
    players = session.get('players', [])
    return jsonify(players)


@app.route('/upload-template', methods=['POST'])
def upload_template():
    # Check if the post request has the file part named 'template'
    if 'template' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    template = request.files['template']
    if template.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if template:
        # Construct a secure filename by allowing only certain characters
        filename = ''.join(c for c in template.filename if c.isalnum() or c in '._- ')
        template_path = os.path.join('uploads', filename)
        template.save(template_path)
        session['template_path'] = template_path  # Save the template path in the session
        return jsonify({'success': True, 'message': 'Template successfully uploaded'}), 200
    else:
        return jsonify({'success': False, 'message': 'Template upload failed'}), 400














""" 
@app.route('/uploader', methods=['POST'])
def upload_file_and_process():
    selected_players = request.json['selectedPlayers']
    template = request.files['template']
    output_path = 'path/to/output/image.png'  # Define your output path

    # Save the template image temporarily
    template_path = os.path.join('uploads', template.filename)
    template.save(template_path)

    # Process the image with the selected players
    process_selected_players_image(selected_players, template_path, output_path)

    return send_file(output_path, as_attachment=True)


@app.route('/create-convo', methods=['POST'])
def create_convo():
    player_data = request.json['players']
    # Your logic to generate the image with player names and numbers
    # Save the image or hold it in memory

    # Return the image
    return send_file(image_path_or_object, mimetype='image/png', as_attachment=True, download_name='convo_image.png')
 """