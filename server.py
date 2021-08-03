import instaloader

from flask import Flask, request, jsonify
from utils.logger import write_log
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# all users profile are connected
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
    return 'InstaData Server Running 🤳'


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


@app.route('/getmyfollowers', methods=['GET'])
@cross_origin()
def get_my_followers():
    write_log('info', 'start getmyfollowers route')
    username = request.json["username"]
    profile = get_profile(username)
    followers = profile.get_followers()
    result = []
    for follower in followers:
        result.append(follower.username)
    result = [str(x) for x in result]
    return jsonify(result)


@app.route('/getmyfollowings', methods=['GET'])
@cross_origin()
def get_my_followings():
    write_log('info', 'start getmyfollowing route')
    username = request.json["username"]
    profile = get_profile(username)
    followings = profile.get_followees()
    result = []
    for following in followings:
        result.append(following.username)
    result = [str(x) for x in result]
    return jsonify(result)


@app.route('/getmyimgprofile', methods=['GET'])
@cross_origin()
def get_my_img_profile():
    write_log('info', 'start getmyimgprofile route')
    username = request.json["username"]
    print(username)
    profile = get_profile(username)
    return profile.profile_pic_url


@app.route('/getmyposts', methods=['GET'])
@cross_origin()
def get_my_posts():
    write_log('info', 'start getmyposts route')
    username = request.json["username"]
    profile = get_profile(username)
    posts = profile.get_posts()
    data = []
    for post in posts:
        data.append((post.url, post.likes, post.comments, post.mediaid))
    return jsonify(data)


if __name__ == '__main__':
    app.run()
