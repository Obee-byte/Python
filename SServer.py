from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    timestamp = int(time.time())  # получаем текущее время в секундах
    file_type = request.form.get('type')  # получаем тип файла из параметра 'type'

    if file_type == 'screenshot':
        filename = f'screenshot_{timestamp}.webp'
    elif file_type == 'text':
        filename = f'text_{timestamp}.txt'
    else:
        return 'Unsupported file type'

    file = request.files['file']
    file.save(filename)
    return 'Screenshot saved successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 