
from http.client import NOT_FOUND
import re
from werkzeug.exceptions import BadRequest
import zipfile
import cv2
from flask import Flask, jsonify, render_template, request, send_file,Response, send_from_directory
from flask_cors import CORS, cross_origin
from flask import Response
import torch
from werkzeug.utils import secure_filename

import google.generativeai as genai
import PIL.Image
import os
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



genai.configure(api_key='')

gemini_model = genai.GenerativeModel('gemini-pro-vision')


app = Flask(__name__)
CORS(app, resources={r"/AntennaType": {"origins": "https://romaroai.netlify.app/"}})
cors = CORS(app, resources={r"/download-image": {"origins": "https://romaroai.netlify.app/"}})

CORS(app, resources={r"/download-script": {"origins": "https://romaroai.netlify.app/"}})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER   


uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

def process_image(img_path):
    img = PIL.Image.open(img_path)
    prompt = ["What type of TV antenna is this?", img]
    response = gemini_model.generate_content(prompt)
    response.resolve()
    print(response.text)


    substrings_to_check = ['TV', 'television']
    dwg_path = None  


    if any(substring in response.text for substring in substrings_to_check):
        generate_TV_autolisp_script('./generated_script.lsp')
        dwg_path = '../uploads/TV_Antenna.dwg'  

    substrings_to_check = ['pylon','cylindrical']
    if any(substring in response.text for substring in substrings_to_check):
        generate_pylon_antenna_script('./generated_script.lsp')
        dwg_path = '../uploads/Pylon_Antenna.dwg' 

    
    substrings_to_check = ['dish', 'parabolic','satellite']
    if any(substring in response.text for substring in substrings_to_check):    
        generate_parabolic_antenna_script('./generated_script.lsp')
        dwg_path = '../uploads/Parabolic_Antenna.dwg' 

    if dwg_path is not None:
        return os.path.join(app.config['UPLOAD_FOLDER'], dwg_path)
    else:
        return None  

def AntennaType(img_path):
    img = PIL.Image.open(img_path)
    prompt = ["What type of TV antenna is this?", img]
    response = gemini_model.generate_content(prompt)
    response.resolve()
    first_sentence = re.split(r'(?<=[.!?])\s+', response.text)[0]

    return first_sentence




def perform_object_detection_yolov5(image_path):
    model = torch.hub.load('ultralytics/yolov5:v6.0', 'yolov5s', pretrained=True)

    img = cv2.imread(image_path)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model([img_rgb])

    img_show = results.xyxy[0].cpu().numpy()
    for box in img_show:
        x_min, y_min, x_max, y_max, conf, _ = box
        cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
    output_path = 'generated_image_with_boxes.jpg'

    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return output_path



def generate_parabolic_antenna_script(output_file):
    autolisp_template = """
    (defun c:CreateParabolicAntenna ()
        ; Define values for the parabolic antenna
        (setq basePoint '(10.0 10.0 0.0)) ; Replace with your desired base point (X, Y, Z)
        (setq dishHeight 5.0) ; Replace with the height of the dish
        (setq dishRadius 8.0) ; Replace with the radius of the dish
        (setq focalLength 6.0) ; Replace with the focal length of the parabolic dish

        ; Calculate the focal point based on the base point and focal length
        (setq focalPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) focalLength)))
        (command "_CIRCLE" Center (0 0) Radius 100)
        (command "_TRIM" Entity (entsel) First (entsel) Second (entsel))
        (command "_CIRCLE" Center (0 0) Radius 50)
        (command "_TRIM" Entity (entsel) First (entsel) Second (entsel))
        (command "_RECTANGLE" First (-50 50) Second (50 -50))
        (command "_RECTANGLE" First (-50 50) Second (50 -50))
        (command "_EXTEND" Entity (entsel) Second (entsel) Third (list (getpoint "\nSpecify endpoint of extension line: "))
        (command "_EXTEND" Entity (entsel) Second (entsel) Third (list (getpoint "\nSpecify endpoint of extension line: ")))
        (command "_CIRCLE" Center (0 0) Radius 2)

        ; Draw the parabolic dish as a 3D solid (SURFACE)
        (command "SOLIDSURF" "REVOLVE" "PARABOLA" "YES" basePoint dishRadius "NO" "360" "")

        ; Draw a line representing the feed antenna at the focal point
        (command "LINE" focalPoint focalPoint "")

        ; Save the drawing (optional)
        (command "SAVEAS" "ParabolicAntennaDrawing" "DWG")

        ; Close AutoCAD (optional)
        (command "QUIT" "Y")
    )

    ; Run the script immediately upon loading
    (c:CreateParabolicAntenna)
    """
    with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file), 'w') as file:
        file.write(autolisp_template)

def generate_pylon_antenna_script(output_file):
    autolisp_template = """
    (defun c:CreatePylonAntenna ()
        ; Define values for the pylon antenna
        (setq basePoint '(10.0 10.0 0.0)) ; Replace with your desired base point (X, Y, Z)
        (setq pylonHeight 15.0) ; Replace with the height of the pylon
        (setq pylonRadius 3.0) ; Replace with the radius of the pylon

        ; Draw the pylon antenna as a cylinder
        (command "CYLINDER" basePoint pylonHeight pylonRadius)

        ; Save the drawing (optional)
        (command "SAVEAS" "PylonAntennaDrawing" "DWG")

        ; Close AutoCAD (optional)
        (command "QUIT" "Y")
    )

    ; Run the script immediately upon loading
    (c:CreatePylonAntenna)
    """
    with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file), 'w') as file:
        file.write(autolisp_template)

def generate_TV_autolisp_script(output_file):
    autolisp_template = """
    (defun c:CreateTVAntenna ()
        ; Define values for the TV antenna
        (setq basePoint '(10.0 10.0 0.0)) ; Replace with your desired base point (X, Y, Z)
        (setq mastHeight 10.0) ; Replace with the height of the mast
        (setq elementsHeight 5.0) ; Replace with the height of the antenna elements
        (setq elementLength 4.0) ; Replace with the length of each antenna element

        ; Calculate the endpoint of the mast
        (setq mastEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight)))

        ; Draw the mast as a line
        (command "LINE" basePoint mastEndPoint "")

        ; Draw the TV antenna elements as vertical lines
        (setq antennaStartPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight)))
        (setq antennaEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight elementsHeight)))

        (repeat 4
            (command "LINE" antennaStartPoint antennaEndPoint "")
            (setq antennaStartPoint antennaEndPoint)
            (setq antennaEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight elementsHeight)))
        )

        ; Save the drawing (optional)
        (command "SAVEAS" "TVAntennaDrawing" "DWG")

        ; Close AutoCAD (optional)
        (command "QUIT" "Y")
    )

    ; Run the script immediately upon loading
    (c:CreateTVAntenna)
    """
    with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file), 'w') as file:
        file.write(autolisp_template)

@app.route('/AntennaType', methods=['GET','POST'])
@cross_origin(origin='https://romaroai.netlify.app', headers=['Content-Type', 'Authorization'])

def handle_antenna_type():
    img_file = request.files.get('image') 

    if not img_file:
        return Response('Invalid image data', status=400, content_type='text/plain')

    filename = secure_filename(img_file.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img_file.save(img_path)

    response_text = AntennaType(img_path)

    output_path = perform_object_detection_yolov5(img_path)

    return Response(response_text, content_type='text/plain', headers={'image-path': output_path})

@app.route('/download-image', methods=['GET','POST'])
@cross_origin(origin='https://romaroai.netlify.app', headers=['Content-Type', 'Authorization'])

def download_image():
    img_file = request.files.get('image')

    if not img_file:
        return Response('Invalid image data', status=400, content_type='text/plain')

    filename = secure_filename(img_file.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img_file.save(img_path)

    output_path = perform_object_detection_yolov5(img_path)

    return send_file(os.path.join(os.getcwd(), 'generated_image_with_boxes.jpg'), as_attachment=True, download_name='generated_image_with_boxes.jpg')


@app.route('/download-script', methods=['GET', 'POST'])
@cross_origin(origin='https://romaroai.netlify.app', headers=['Content-Type', 'Authorization'])
def upload_and_download():
    if 'image' not in request.files:
        return Response('No image part', status=400, content_type='text/plain')

    img_file = request.files['image']

    if img_file.filename == '':
        return Response('No selected image file', status=400, content_type='text/plain')

    if img_file and allowed_file(img_file.filename):
        filename = secure_filename(img_file.filename)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img_file.save(img_path)

        # Process the uploaded image and generate AutoLISP script
        dwg_path = process_image(img_path)

        if dwg_path is None:
            return Response('Failed to generate DWG file', status=500, content_type='text/plain')

        # Check if the file exists before attempting to get its stat
        if os.path.exists(dwg_path):
            try:
                st = os.stat(dwg_path)

                # Create a ZIP file containing both DWG and AutoLISP script
                zip_filename = 'generated_files.zip'
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    zipf.write(dwg_path, arcname='generated_drawing.dwg')
                    zipf.write(os.path.join(app.config['UPLOAD_FOLDER'], 'generated_script.lsp'), arcname='generated_script.lsp')

                # Return the ZIP file
                return send_file(zip_filename, as_attachment=True, download_name='generated_files.zip', mimetype='application/zip')

            except Exception as e:
                print(f"Error getting AutoLISP script and DWG file: {str(e)}")
                return Response('Error getting AutoLISP script and DWG file', status=500, content_type='text/plain')
        else:
            return NOT_FOUND(f'DWG file not found at path: {dwg_path}')

    else:
        return Response('Invalid file type', status=400, content_type='text/plain')
if __name__ == '__main__':
    app.run(debug=True)