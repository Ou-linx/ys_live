from flask import Flask, request, make_response, abort
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# @app.route('/api/<path:subpath>', methods=['GET', 'POST'])
# def api(subpath):


@app.route('/')
def index():
    return "<h1>Hello friend</h1>"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=7878, debug=False)
