from flask import Flask, render_template, session, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def index():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
