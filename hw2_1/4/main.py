from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def index():
    return "hello, docker!"

app.run(host='0.0.0.0', port=3000)
