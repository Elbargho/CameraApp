async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

async function loginBtnClicked() {
    let username = document.querySelector('#username').value;
    let password = await sha256(document.querySelector('#password').value);
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