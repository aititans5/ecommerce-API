
from flask import Blueprint, request, jsonify
from ftplib import FTP

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

#from src.database import logindetail, db
#from flasgger import swag_from

upload = Blueprint("UploadImage", __name__, url_prefix="/api/v1/upload")

FTP_HOST = '192.168.56.1'
FTP_USERNAME = 'ftp_user'
FTP_PASSWORD = 'Abhi123@.'
FTP_PATH = 'ftp://192.168.56.1'

@upload.post('/UploadImage')
def addUploadImageToFtp():
    # add image to ftp folder.


    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        # Connect to the FTP server
        with FTP(FTP_HOST) as ftp:
            ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
            str = f'STOR {image_file.filename}'
            # Upload the image to the FTP server
            ftp.storbinary(str, image_file)

        return jsonify({'message': 'Image uploaded to FTP successfully'}), HTTP_200_OK

    except Exception as e:
        print(f'Error uploading image to FTP: {e}')
        return jsonify({'error': 'Failed to upload image to FTP'}), HTTP_500_INTERNAL_SERVER_ERROR




