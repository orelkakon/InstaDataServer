import instaloader

from flask import Flask, request
from utils.logger import write_log
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# all users are connected
profiles = []


def get_profile(username):
    for profile in profiles:
        if profile[0] == username:
            return profile[1]
    return None


def delete_profile(username):
    for profile in profiles:
        if profile[0] == username:
            profiles.remove(profile)
            return


@app.route('/')
@cross_origin()
def hello():
    return 'Welcome InstaData Server'


@app.route('/sanity')
@cross_origin()
def sanity():
    write_log('info', 'start sanity route')
    return 'InstaData Server Running'


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    write_log('info', 'start login route')
    username = request.json["username"]
    password = request.json["password"]
    write_log('info', username + ", " + password + " - try to connect")
    insta_data = instaloader.Instaloader()
    try:
        insta_data.login(username, password)
        profile = instaloader.Profile.from_username(insta_data.context, username)
        profiles.append((username, profile))
        return 'success'
    except:
        write_log('info', 'wrong details')
        return 'failed'


@app.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    write_log('info', 'start logout route')
    username = request.json["username"]
    delete_profile(username)
    return 'success'


if __name__ == '__main__':
    app.run()
