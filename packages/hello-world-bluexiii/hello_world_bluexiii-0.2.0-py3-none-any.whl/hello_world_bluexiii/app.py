from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return 'Hello from Flask!'

def run_app():
    app.run(debug=True, port=3000)
