/**
 * Created by suli on 6/25/17.
 */
//消息闪现
function fade() {
    //$("#flashes").fadeOut('fast');
}

function showLogin() {
    document.getElementById('light').style.display = 'block';
}
function hideLogin() {
    document.getElementById('light').style.display = 'none';
}
function showRegister() {
    document.getElementById('light').style.display = 'none';
    /*document.getElementById('register').style.display = 'block'*/
    window.location.href = "/register"
}

function hideRegister() {
    document.getElementById('register').style.display = 'none';
}