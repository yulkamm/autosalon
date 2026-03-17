from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>IT WORKS!</h1><p>Flask is running!</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
