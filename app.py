from flask import Flask, render_template, session, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def index():
    return render_template('login.html')


@app.route("/login")
def login():
    try:
        data = request.args
        res = requests.get(
            f'https://usersignin.azurewebsites.net/api/login?username={data["username"]}&password={data["password"]}').json()
        if(res['res'] != 'ok'):
            return redirect(url_for('loginFailed'))
        else:
            session['username'] = data['username']
            session['password'] = data['password']
            return redirect(url_for('cameraApp'))
    except Exception as e:
        return {"server encountered an internal error"}, 500


@app.route("/loginfailed")
def loginFailed():
    return render_template('loginFailed.html')


@app.route("/cameraApp")
def cameraApp():
    if 'password' in session:
        return render_template('cameraApp.html')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
