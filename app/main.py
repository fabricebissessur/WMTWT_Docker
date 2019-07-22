from flask import Flask, url_for, request, render_template
import requests

app = Flask(__name__)

wsgi_app = app.wsgi_app

@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

