import os
import secrets
import io
from flask import Flask, request, send_file, jsonify, render_template
from Cryptodome.Cipher import AES

app = Flask(__name__)

# Encryption Settings
AES_KEY_LEN = 32  # 256 bits
IV_LEN = 16
TAG_LEN = 16

# Limit upload size to 100MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate-key', methods=['GET'])
def generate_key():
    return jsonify({"key": secrets.token_hex(AES_KEY_LEN)})


@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    file = request.files.get('file')
    key_hex = request.form.get('key') or secrets.token_hex(AES_KEY_LEN)

    if not file:
        return jsonify({"error": "No files uploaded."}), 400

    try:
        key = bytes.fromhex(key_hex)
        file_data = file.read()

        # AES-GCM Encryption
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(file_data)

        result = cipher.nonce + tag + ciphertext

        return send_file(
            io.BytesIO(result),
            mimetype='application/octet-stream',
            download_name=f"{file.filename}.enc",
            as_attachment=True
        ), 200, {'X-Key': key_hex, 'Access-Control-Expose-Headers': 'X-Key'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    file = request.files.get('file')
    key_hex = request.form.get('key')

    if not file or not key_hex:
        return jsonify({"error": "Missing file or key"}), 400

    try:
        key = bytes.fromhex(key_hex)
        raw_data = file.read()

        nonce = raw_data[:IV_LEN]
        tag = raw_data[IV_LEN:IV_LEN + TAG_LEN]
        ciphertext = raw_data[IV_LEN + TAG_LEN:]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

        original_name = file.filename.replace('.enc', '')

        return send_file(
            io.BytesIO(decrypted_data),
            mimetype='application/octet-stream',
            download_name=original_name,
            as_attachment=True
        )
    except Exception:
        return jsonify({"error": "Invalid key or corrupted file"}), 400


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify({"error": "File too large. Maximum size is 100MB."}), 413


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)