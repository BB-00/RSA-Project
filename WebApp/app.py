from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('', 'index.html')


@app.route('/start')
def start():

    return ''

@app.route('/stop')
def stop():

    return ''

@app.route('/js/<path:path>')
def serveJS(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def serveIMG(path):
    return send_from_directory('img',path)
