from flask import Flask
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Create Flask app
app = Flask(__name__)

# Hello World route
@app.route('/')
def hello_world():
    return 'Hello World'

# Start in production mode
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)