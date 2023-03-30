from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)



@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["username"]
        contact = request.form["phone_no"]
        message = request.form["message"]
        is_message_sent = True
        send_email(email, name, contact, message)

        return render_template("contact.html", message_sent=True)

    return render_template("contact.html", message_sent=False)


def send_email(email,name, contact, message):
    MY_EMAIL = "yeshacodes@gmail.com"
    MY_PASSWORD = "yujjfkqvdfwdtnrr"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject: A message was sent through your contact info\n\n Name: {name} \n Email: {email} \n Contact: {contact} \n Message: {message}")















if __name__ == "__main__":

    app.run(debug=True)
