let carInPark = false;

async function server_request(method, url, obj = null) {
    baseUrl = window.location.origin;
    let [status, data] = await fetch(`${baseUrl}/${url}`,
        {
            method: method,
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            body: (method == 'POST') ? JSON.stringify(obj) : null
        }).then(res => {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error(res.statusText);
            }
        }).then(jsonResponse => {
            return [true, jsonResponse];
        }
        ).catch((err) => { return [false, err]; });
    return [status, data];
}

async function stateChanger(json) {
    let results = json['results'];
    let plateViewer = document.getElementById('plateViewer');
    let onwerMsg = document.getElementById('ownerMsg');
    if (results.length > 0 && carInPark == false) { // a car entered
        let plateNumber = results[0]['plate'];
        plateViewer.innerText = plateNumber;
        [res, data] = await server_request('POST', 'carentered', {'platenumber': plateNumber});
        if(res){
            onwerMsg.innerText = data['msg']
        }else{
            alert('server encountered an internal error');
        }
    } else if (results.length == 0 && carInPark == true) { // a car left
        plateViewer.innerText = '-------';
        [res, data] = await server_request('POST', 'carleft');
        if(res){
            onwerMsg.innerText = data['msg']
        }else{
            alert('server encountered an internal error');
        }
    }
}
