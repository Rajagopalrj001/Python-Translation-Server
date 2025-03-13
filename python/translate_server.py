# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from googletrans import Translator
# import os

# app = Flask(__name__)

# CORS(app)  # Enable CORS for all routes

# translator = Translator()

# @app.route('/translate', methods=['POST'])
# def translate():
#     try:
#         data = request.get_json()
#         text = data.get('text', '')
#         target_lang = data.get('target_lang', 'en')
        
#         translation = translator.translate(text, dest=target_lang)
        
#         return jsonify({
#             'translation': translation.text,
#             'source_lang': translation.src,
#             'target_lang': translation.dest
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)


from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
translator = Translator()

# Function to check if input is Tanglish
def is_tanglish(text):
    tamil_chars = "அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவழளறன"  # Tamil letters
    return not any(char in tamil_chars for char in text)

# Function to convert Tanglish to Tamil script
def convert_tanglish_to_tamil(text):
    return transliterate(text, sanscript.ITRANS, sanscript.TAMIL)  # Converts Tanglish to Tamil

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'en')  # Default target language is English

        # Handle Tanglish specifically
        if is_tanglish(text):
            tamil_script = convert_tanglish_to_tamil(text)  # Convert Tanglish to Tamil script
            translation = translator.translate(tamil_script, dest=target_lang)  # Translate Tamil to English
        else:
            translation = translator.translate(text, dest=target_lang)  # Normal translation for other languages

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
