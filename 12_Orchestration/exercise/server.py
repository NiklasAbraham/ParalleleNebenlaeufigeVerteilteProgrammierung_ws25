from flask import Flask

app = Flask(__name__)
counter = 0

@app.route('/put/<int:value>')
def put_counter(value):
    global counter
    counter = value
    return ""

@app.route('/get')
def get_counter():
    return f"{counter}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
