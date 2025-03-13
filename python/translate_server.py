from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
import os

app = Flask(__name__)
# Allow requests from your frontend application
CORS(app, origins=["http://127.0.0.1:5175/","http://127.0.0.1:3000/"])  # Add your production URL

translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'en')
        
        translation = translator.translate(text, dest=target_lang)
        
        return jsonify({
            'translation': translation.text,
            'source_lang': translation.src,
            'target_lang': translation.dest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)