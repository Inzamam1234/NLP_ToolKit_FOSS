import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from utils.inference import T5Inference


load_dotenv()


MODEL_DIR = os.getenv('MODEL_DIR', 'model') # default to local ./model
PORT = int(os.getenv('PORT', 5000))


app = Flask(__name__)
CORS(app)


# Initialize model once
print('Loading model from:', MODEL_DIR)
model = T5Inference(MODEL_DIR)


@app.route('/')
def index():
return render_template('index.html')


@app.route('/api/summarize', methods=['POST'])
def summarize():
data = request.json or {}
text = data.get('text', '')
if not text.strip():
return jsonify({'error': 'Empty input'}), 400
# Optional parameters
max_length = int(data.get('max_length', 150))
min_length = int(data.get('min_length', 20))
summary = model.run_task(text, task='summarize', max_length=max_length, min_length=min_length)
return jsonify({'result': summary})


@app.route('/api/paraphrase', methods=['POST'])
def paraphrase():
data = request.json or {}
text = data.get('text', '')
if not text.strip():
return jsonify({'error': 'Empty input'}), 400
num_return_sequences = int(data.get('num_return_sequences', 1))
paraphrased = model.run_task(text, task='paraphrase', num_return_sequences=num_return_sequences)
return jsonify({'result': paraphrased})


@app.route('/api/grammar', methods=['POST'])
def grammar():
data = request.json or {}
text = data.get('text', '')
if not text.strip():
return jsonify({'error': 'Empty input'}), 400
corrected = model.run_task(text, task='grammar')
return jsonify({'result': corrected})


if __name__ == '__main__':
app.run(host='0.0.0.0', port=PORT, debug=True)