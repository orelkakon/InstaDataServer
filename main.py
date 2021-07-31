import instaloader
import operator
from tkinter import *
import tkinter.messagebox


#  Quit
def Quit(newWindow):
    tkinter.messagebox.showinfo('QUIT', 'Bye-Bye')
    newWindow.quit()


# Logout
def Logout(NW, root):
    root.deiconify()
    NW.withdraw()
    E2.delete(0, 'end')
    E1.delete(0, 'end')


def getStatisticsFollowers(profile):
    FWS = profile.get_followers()
    FNG = profile.get_followees()
    notFollowYouBack = []
    youNotFollowBack = []
    for followin in FNG:  # my following
        if followin not in FWS:
            notFollowYouBack.append(followin.username)
    FWS = profile.get_followers()
    FNG = profile.get_followees()
    for follow in FWS:  # my followers
        if follow not in FNG:
            youNotFollowBack.append(follow.username)
    ratio = FWS.total_index/FNG.total_index
    notFollowYouBack = [str(x) for x in notFollowYouBack]
    msg1 = ', '.join(notFollowYouBack)
    youNotFollowBack = [str(x) for x in youNotFollowBack]
    msg2 = ', '.join(youNotFollowBack)
    tkinter.messagebox.showinfo("Statistics: ", 'Followers: ' + str(FWS.total_index) + '\n' +
                                'Followings: ' + str(FNG.total_index) + '\n' +
                                'They are not follow you back: \n' + msg1 + '\n' +
                                'You are not follow back: \n' + msg2 + '\n' +
                                'RATIO is: ' + str(ratio))


def option5(profile):
    getStatisticsFollowers(profile)


def getListUsersLikes(profile, maxNum):
    users = {}
    posts = profile.get_posts()
    num = min(int(maxNum), posts.count)
    for post in posts:
        if num > 0:
            num -= 1
            post_likes = post.get_likes()
            for likee in post_likes:
                if likee.username in users:
                    new_number = users[likee.username] + 1
                    users[likee.username] = new_number
                else:
                    users.update({likee.username: 1})
    return users


def getUserMostLiked(profile, num, frame):
    users = getListUsersLikes(profile, num)
    user = max(users.items(), key=operator.itemgetter(1))[0]
    tkinter.messagebox.showinfo('MOST LIKES:', 'The user is: ' + user + '. \nhe give you '+str(users[user])+' likes')
    frame.pack_forget()


def option1(profile, newWindow):
    frame = Frame(newWindow)
    frame.pack()
    L3 = Label(frame, text="Insert how many posts to go over")
    L3.pack()
    E3 = Entry(frame, bd=5)
    E3.pack()
    Button(frame, text="search",
           command=lambda: getUserMostLiked(profile, E3.get(), frame), bg='green').pack()


def getListUserscomments(profile, maxNum):
    users = {}
    posts = profile.get_posts()
    num = min(int(maxNum), posts.count)
    for post in posts:
        if num > 0:
            num -= 1
            post_comments = post.get_comments()
            for comment in post_comments:
                if comment.owner.username in users:
                    new_number = users[comment.owner.username] + 1
                    users[comment.owner.username] = new_number
                else:
                    users.update({comment.owner.username: 1})
    return users


def getUserMostCommented(profile, num, frame):
    users = getListUserscomments(profile, num)
    user = max(users.items(), key=operator.itemgetter(1))[0]
    tkinter.messagebox.showinfo('MOST COMMENTS:', 'The user is: ' + user + '. \nhe give you '+str(users[user])+' comments')
    frame.pack_forget()


def option2(profile, newWindow):
    frame = Frame(newWindow)
    frame.pack()
    L3 = Label(frame, text="Insert how many posts to go over")
    L3.pack()
    E3 = Entry(frame, bd=5)
    E3.pack()
    Button(frame, text="search",
           command=lambda: getUserMostCommented(profile, E3.get(), frame), bg='green').pack()


def getCommentsAndLikesOfSpecificUser(profile, user, frame):
    Likes = 0
    Comments = 0
    for post in profile.get_posts():
        post_comments = post.get_comments()
        for comment in post_comments:
            if comment.owner.username == user:
                Comments += 1
        post_likes = post.get_likes()
        for like in post_likes:
            if like.username == user:
                Likes += 1
    tkinter.messagebox.showinfo('LIKES & COMMENTS of '+user+':',
                                user + ' give you ' + str(Likes) + ' likes. \nand ' + str(Comments) + ' comments.')
    frame.pack_forget()


def option3(profile, newWindow):
    frame = Frame(newWindow)
    frame.pack()
    L3 = Label(frame, text="Insert username go check")
    L3.pack()
    E3 = Entry(frame, bd=5)
    E3.pack()
    Button(frame, text="search",
           command=lambda: getCommentsAndLikesOfSpecificUser(profile, E3.get(), frame), bg='green').pack()


def getTop10(profile, num, frame):
    likesList = getListUsersLikes(profile, num)
    commentsList = getListUserscomments(profile, num)
    top10likes = dict(sorted(likesList.items(), key=operator.itemgetter(1), reverse=True)[:10])
    top10comments = dict(sorted(commentsList.items(), key=operator.itemgetter(1), reverse=True)[:10])
    top10likes = [str(x) for x in top10likes]
    msg1 = ', '.join(top10likes)
    top10comments = [str(x) for x in top10comments]
    msg2 = ', '.join(top10comments)
    tkinter.messagebox.showinfo('TOP 10 LIKES & COMMENTS:',
                                'Likes: \n' + msg1 + '\n'
                                'Comments: \n' + msg2)
    frame.pack_forget()


def option4(profile, newWindow):
    frame = Frame(newWindow)
    frame.pack()
    L3 = Label(frame, text="Insert how many posts to go over")
    L3.pack()
    E3 = Entry(frame, bd=5)
    E3.pack()
    Button(frame, text="search",
           command=lambda: getTop10(profile, E3.get(), frame), bg='green').pack()


root = Tk()
root.geometry("300x250")
root.title('Home Page')
#  title
var1 = StringVar()
label1 = Label(root, textvariable=var1, relief=RAISED, bd=5, bg='blue')
var1.set("WELCOME INSTAGRAM CALCULATOR")
label1.pack()
#  username
L1 = Label(root, text="Username:")
L1.pack()
E1 = Entry(root, bd=5)
E1.pack()
#  password
L2 = Label(root, text="Password:")
L2.pack()
E2 = Entry(root, bd=5, show="*")
E2.pack()


#  login
def login():
    L = instaloader.Instaloader()
    L.login(E1.get(), E2.get())
    profile = instaloader.Profile.from_username(L.context, E1.get())
    tkinter.messagebox.showinfo("Successful Login!", "Welcome " + E1.get())
    newWindow = Toplevel(root)
    newWindow.title("Menu Page")
    newWindow.geometry("400x300")
    root.withdraw()
    Label(newWindow, text="Menu Actions - Choose action from list below", bd=3, bg='blue').pack()
    op2 = Button(newWindow, text="Find the user who has commented to you the most times", bg='yellow',
                 command=lambda: option2(profile, newWindow)).pack()
    op3 = Button(newWindow, text="Get how many likes and comments of specific username", bg='yellow',
                 command=lambda: option3(profile, newWindow)).pack()
    op5 = Button(newWindow, text="Get statistics of ratio on followers/following", bg='yellow',
                 command=lambda: option5(profile)).pack()
    op1 = Button(newWindow, text="Find the user who did the most likes for you", bg='yellow',
                 command=lambda: option1(profile, newWindow)).pack()
    op4 = Button(newWindow, text="Get top 10 likes and comments", bg='yellow',
                 command=lambda: option4(profile, newWindow)).pack()
    op6 = Button(newWindow, text="Logout", command=lambda: Logout(newWindow, root), bg='orange').pack()
    op6 = Button(newWindow, text="Quit", command=lambda: Quit(newWindow), bg='red').pack()


B = Button(root, text="get in", command=login, bg='green')
B.pack()

root.mainloop()
