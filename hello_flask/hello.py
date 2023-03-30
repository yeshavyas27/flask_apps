from flask import Flask

def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper

def make_underline(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper




app = Flask(__name__)



@app.route("/")
@make_bold
@make_emphasis
@make_underline
def hello_world():
    return "<h1 style='text-align: center';'color: brown'>Hello, World!</h1>" \
           "<p>This is a paragraph</p>" \
           "<img src='https://media.giphy.com/media/uWYjSbkIE2XIMIc7gh/giphy.gif' alt='kitten_image'>"

@app.route("/bye")
def byee():
    return "<p>Byee folks haha!!</p>"

#getting hold of what user types in url
@app.route("/<username>")
def say_hello(username):
    return f"Hello there {username}!"

if __name__ == "__main__":
    app.run(debug=True)

