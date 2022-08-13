from flask import Flask, render_template, session, request, redirect, url_for
import requests
from azure.data.tables import TableClient

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
            session['platenumber'] = res['platenumber']
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


def getParkLocation():
    table_client = TableClient.from_connection_string(
        conn_str="DefaultEndpointsProtocol=https;AccountName=generalstoragetable;AccountKey=85HME4uxdE6PSsdXv6Dv9UibBpbBg2JRqGj3m8AdVsNdGu8wcw+0zcpOsq4LJDHRUVSiyfAAKz3A+AStgkToBQ==;EndpointSuffix=core.windows.net", table_name="Parks")
    entities = table_client.query_entities(
        f"PartitionKey eq '{session['username']}'")
    entity = list(entities)
    if(entity != []):
        return True, entity[0]['RowKey']
    else:
        return False, None


def getReserver(location):
    table_client = TableClient.from_connection_string(
        conn_str="DefaultEndpointsProtocol=https;AccountName=generalstoragetable;AccountKey=85HME4uxdE6PSsdXv6Dv9UibBpbBg2JRqGj3m8AdVsNdGu8wcw+0zcpOsq4LJDHRUVSiyfAAKz3A+AStgkToBQ==;EndpointSuffix=core.windows.net", table_name="Requests")
    entities = table_client.query_entities(f"RowKey eq '{location}'")
    entity = list(entities)
    if(entity != []):
        return True, entity[0]['PartitionKey'], entity[0]['platenumber']
    else:
        return False, None, None


@app.route('/carentered', methods=["POST"])
def carEntered():
    try:
        msg = ''
        status = False
        data = request.get_json()
        inParkPn = data['platenumber']
        hasPark, location = getParkLocation()
        hasReserver, reserverUn, reserverPn = getReserver(location)
        if inParkPn == session['platenumber'] or not hasPark:
            msg = 'Owner has entered the park'
        elif not hasReserver or reserverPn != inParkPn:
            msg = f'A car with platenumber {inParkPn} entered your park without reservation'
            # signalR(owner, msg)
        else:
            msg = f'The reserver has entered the park'
            session['reserver'] = reserverUn
            status = True
            # signalR(owner, msg)
        session['stats'] = status
        return {'msg': msg}
    except:
        return {}, 500


@app.route('/carleft', methods=["POST"])
def carLeft():
    try:
        msg = ''
        if(not session['status']):
            msg = 'Car has left'
            # signalR(owner, msg)
        else:
            res = requests.get(
                f'http://releasepark.azurewebsites.net/api/releasepark?location={session["location"]}&username={session["username"]}&password={session["password"]}').json()
            if(res['res'] != 'ok'):
                raise Exception
            msg = f'Car has left and you received {res["bill"]}$'
        return {'msg': msg}
    except:
        return {}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
