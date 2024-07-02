import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

#accesskey는 카톡에 저장되어있음.! s3비번도 
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIA47CR2RIJTJZY367M',
    region_name='ap-northeast-1'
)

UPLOAD_BUCKET = 'uploadimage-bucket'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    email = request.form.get('email')
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        s3_client.upload_fileobj(file, UPLOAD_BUCKET, filename)
        s3_url = f"https://{UPLOAD_BUCKET}.s3.amazonaws.com/{filename}"
        return jsonify({"email": email, "file_path": s3_url}), 201

if __name__ == '__main__':
    app.run(port=5001)