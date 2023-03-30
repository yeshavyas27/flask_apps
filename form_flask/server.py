from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login_page():
    user_name = request.form['username']
    password = request.form['password']

    return f"Hello {user_name} Your password: {password}"


if __name__ == "__main__":
    app.run(debug=True)

