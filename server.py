from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def sanity():
    return 'InstaData Server Running'


@app.route('/login', methods=['POST'])
def login():
    args = request.json["username"]
    return args


if __name__ == '__main__':
    app.run()
