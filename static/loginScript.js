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