from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/AmeenInt/dl/insta', methods=['GET'])
def download_instagram_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": 400, "error": "No URL provided"}), 400

    try:
        encoded_url = requests.utils.quote(url)
        api_url = f"https://saveinsta.io/dl.php?url={encoded_url}"

        response = requests.get(api_url)
        
        if response.status_code == 200:
            media_url = response.url
            return jsonify({
                "status": 200,
                "media": [media_url]
            })
        else:
            return jsonify({"status": response.status_code, "error": "Failed to retrieve video"}), response.status_code
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
