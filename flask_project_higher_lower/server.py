from flask import Flask
import random

app = Flask(__name__)

answer = random.randint(0,10)
@app.route("/")
def hello_world():
    return "<h1 style='color:purple'>Guess a number between 0-9</h1>" \
           "<img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGZhOGNmYzMxYjg1N" \
           "DY4Y2JlY2JiMzNmYzlhY2VhYzIyYmEwZTVkYiZjdD1n/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

@app.route("/<int:number>")
def guess(number):
    if (number == answer):
        return "<h1 style='color:purple'>You got it!!!</h1>" \
           "<img src='https://media.giphy.com/media/lkbNG2zqzHZUA/giphy.gif'>"

    elif(number>answer):
        return "<h1 style='color:purple'>Too High</h1>" \
           "<img src='https://media.giphy.com/media/135QXxqZ9d0QGk/giphy.gif'>"
    elif(number<answer):
        return "<h1 style='color:purple'>Too Low</h1>" \
               "<img src='https://media.giphy.com/media/wfS4vDyVsASQygl4mN/giphy.gif'>"


print(answer)

if __name__ == "__main__":
    app.run(debug=True)
