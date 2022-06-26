from flask import Flask, request
from flask_cors import CORS
import requests
import numpy as np
import json
from PIL import Image
import io
import matplotlib.pyplot as plt
from base64 import encodebytes

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def greet():
    return 'Land Cover Segmentation V1.0'
@app.route('/api/v1/predict', methods=['POST'])
def predict_v1():
    land_names = ['Urban land', 'Agriculture land', 'Rangeland', 'Forest land', 'Water', 'Barren land', 'Unknown']
    image = Image.open(request.files['images']).convert('RGB')
    input = np.asarray(image)
    input = np.expand_dims(input, axis=0).astype(np.float32)
    data = json.dumps({
        'signature_name': 'serving_default',
        'instances': input.tolist()
    })
    headers = {'content-type': 'application/json'}
    url = 'http://tensorflowapi:8501/v1/models/land-cover:predict'
    json_response = requests.post(url, data=data, headers=headers, timeout=None)
    preds = json.loads(json_response.text)['predictions']
    preds = np.array(preds)[0]
    
    result = {}
    for i in range(preds.shape[-1]):
        cm = plt.get_cmap('viridis')
        img = Image.fromarray((cm(preds[:, :, i]) * 255).astype(np.uint8))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        result[land_names[i]] = encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return result

if __name__ == '__main__':
    app.run()