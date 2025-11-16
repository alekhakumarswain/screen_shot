from flask import Flask, request, send_file
from flask_cors import CORS
from playwright.sync_api import sync_playwright
import io

app = Flask(__name__)
CORS(app)

@app.route("/snapshot")
def snapshot():
    url = request.args.get("url")
    if not url:
        return "URL missing", 400

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto(url, timeout=60000, wait_until="networkidle")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1500)
        img_bytes = page.screenshot(full_page=False)
        browser.close()

    return send_file(io.BytesIO(img_bytes), mimetype="image/png")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
