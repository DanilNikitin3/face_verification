from flask import Flask, request, jsonify
import os
import sys
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from NN_test.test import test_func


app = Flask(__name__)

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'Нет поля photo'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'Имя файла пустое'}), 400
    
    print(f"Получен файл: {file.filename}, размер: {file.content_length or 'неизвестен'} байт")
    
    file.save('./NN_test/test_image.jpg')

    img = Image.open('./NN_test/test_image.jpg')
    new_img = img.resize((168, 192))

    new_img.save('./NN_test/tests.jpg')

    result = test_func("tests")

    return jsonify({
        'success': True,
        'message': result,
        'filename': file.filename
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

