from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Function to extract the video URL from the Instagram page
def extract_video_url(instagram_url):
    try:
        response = requests.get(instagram_url)
        if response.status_code != 200:
            return None

        video_url = re.search('"video_url":"(.*?)"', response.text)
        if video_url:
            return video_url.group(1).replace("\\u0026", "&")

        return None
    except Exception as e:
        print(f"Error extracting video URL: {e}")
        return None

@app.route('/api/download/insta/reel', methods=['GET'])
def download_instagram_reel():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Please provide a valid Instagram URL.'}), 400

    video_url = extract_video_url(url)
    if video_url:
        return jsonify({'media': video_url}), 200
    else:
        return jsonify({'error': 'Failed to retrieve video from the provided URL.'}), 400

# Entry point for Vercel or Render
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
