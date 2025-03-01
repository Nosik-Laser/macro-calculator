import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to the Macro Calculator!</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment (for deployment)
    app.run(host="0.0.0.0", port=port, debug=True)
