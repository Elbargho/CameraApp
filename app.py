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
            session['ownerUN'] = data['username']
            session['password'] = data['password']
            session['ownerPN'] = res['accDetails']['platenumber']
            return redirect(url_for('cameraApp'))
    except:
        return {"server encountered an internal error"}, 500


@app.route("/loginfailed")
def loginFailed():
    return render_template('loginFailed.html')


@app.route("/cameraApp")
def cameraApp():
    if 'password' in session:
        return render_template('cameraApp.html')
    return redirect(url_for('index'))


def signalR(username, msg):
    requests.get(
        f"https://signalrnotification.azurewebsites.net/api/sendnotification?username={username}&message={msg}")


@app.route('/notifylimit')
def notifyLimit():
    signalR(session['ownerUN'], 'Reserver has less than half hour left')
    signalR(session['reserver'], 'Note that you have less than half hour left')
    return {}, 200


@app.route('/carentered', methods=["POST"])
def carEntered():
    try:
        status = False
        data = request.get_json()
        currPN = data['platenumber']
        res = requests.get(
            f"https://getreserve.azurewebsites.net/api/getReserve?username={session['ownerUN']}&password={session['password']}").json()
        session["location"], session["reserver"], reserverPn, timeLeft = res["location"], res[
            "reserver"], res["platenumber"], res["timeLeft"]
        if currPN == session['ownerPN'] or session["location"] == None:
            msg = 'Owner has entered the park'
        elif session["reserver"] == None or reserverPn != currPN:
            msg = f'A car with platenumber {currPN} entered your park without reservation'
        else:
            msg = f'The reserver has entered the park'
            status = True
        signalR(session["ownerUN"], msg)
        session['status'] = status
        return {'msg': msg, 'status': status, 'timeLeft': timeLeft}, 200
    except:
        return {}, 500


@app.route('/carleft', methods=["POST"])
def carLeft():
    try:
        if(not session['status']):
            msg = 'Car has left'
            signalR(session["ownerUN"], msg)
        else:
            res = requests.get(
                f'http://releasepark.azurewebsites.net/api/releasepark?location={session["location"]}&username={session["ownerUN"]}&password={session["password"]}').json()
            if(res['res'] != 'ok'):
                raise Exception
            msg = f'Car has left and you received {res["bill"]}₪'
        return {'msg': msg}, 200
    except:
        return {}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
