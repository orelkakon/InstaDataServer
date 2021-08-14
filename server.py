import instaloader

from flask import Flask, request, jsonify
from instaloader import TopSearchResults

from utils.logger import write_log
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# all users profile are connected
profiles = []
insta_data = instaloader.Instaloader()


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


@app.route('/getmyfollowers', methods=['POST'])
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


@app.route('/getmyfollowings', methods=['POST'])
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


@app.route('/getmyimgprofile', methods=['POST'])
@cross_origin()
def get_my_img_profile():
    write_log('info', 'start getmyimgprofile route')
    username = request.json["username"]
    profile = get_profile(username)
    return profile.profile_pic_url


@app.route('/getmyposts', methods=['POST'])
@cross_origin()
def get_my_posts():
    write_log('info', 'start getmyposts route')
    username = request.json["username"]
    profile = get_profile(username)
    posts = profile.get_posts()
    data = []
    for post in posts:
        data.append((post.url, post.date, post.likes, post.comments, post.mediaid))
    return jsonify(data)


@app.route('/getmytaggedposts', methods=['POST'])
@cross_origin()
def get_my_tagged_posts():
    write_log('info', 'start getmytaggedposts route')
    username = request.json["username"]
    profile = get_profile(username)
    posts = profile.get_tagged_posts()
    data = []
    for post in posts:
        data.append((post.url, post.owner_username, post.date, post.likes, post.comments, post.mediaid))
    return jsonify(data)


@app.route('/getmysavedposts', methods=['POST'])
@cross_origin()
def get_my_saved_posts():
    write_log('info', 'start getmysavedposts route')
    username = request.json["username"]
    profile = get_profile(username)
    posts = profile.get_saved_posts()
    data = []
    for post in posts:
        data.append((post.url, post.owner_username, post.date, post.likes, post.comments, post.mediaid))
    return jsonify(data)


@app.route('/gettopsearch', methods=['POST'])
@cross_origin()
def get_top_search():
    write_log('info', 'start gettopsearch route')
    search = request.json["search"]
    data = TopSearchResults(insta_data.context, search).get_profiles()
    result = []
    for prof in data:
        result.append(prof.username)
    result = [str(x) for x in result]
    return jsonify(result)


@app.route('/gettoplocation', methods=['POST'])
@cross_origin()
def get_top_location():
    write_log('info', 'start gettoplocation route')
    search = request.json["search"]
    data = TopSearchResults(insta_data.context, search).get_locations()
    result = []
    for location in data:
        result.append(location.name)
    result = [str(x) for x in result]
    return jsonify(result)


@app.route('/gettophashtag', methods=['POST'])
@cross_origin()
def get_top_hashtag():
    write_log('info', 'start gettophashtag route')
    search = request.json["search"]
    data = TopSearchResults(insta_data.context, search).get_hashtag_strings()
    result = []
    for hashtag in data:
        result.append(hashtag)
    result = [str(x) for x in result]
    return jsonify(result)


if __name__ == '__main__':
    app.run()
