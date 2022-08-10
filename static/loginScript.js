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

async function loginBtnClicked() {
    let username = document.querySelector('#username').value;
    let password = document.querySelector('#password').value;
    window.location.replace(`/login?username=${username}&password=${password}`);
}

function openedModal() {
    options = { backdrop: 'static', keyboard: false };
    openedModal = new bootstrap.Modal(document.querySelector('#login'), options);
    openedModal.show();
}

window.onload = () => {
    openedModal();
    document.querySelector('#loginBtn').addEventListener('click', loginBtnClicked);
}