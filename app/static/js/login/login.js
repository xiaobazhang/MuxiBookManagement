/**
 * Created by suli on 6/13/17.
 */
function login() {

    var username = document.getElementById("username");
    var pass = document.getElementById("password");

    if (username.value == "") {

        alert("请输入用户名");

    } else if (pass.value == "") {

        alert("请输入密码");

    } else if (username.value == "admin" && pass.value == "123456") {

        window.location.href = "welcome.html";

    } else {

        alert("请输入正确的用户名和密码！")

    }
}

function showLogin() {
    document.getElementById('content_log').style.display = 'block';
    document.getElementById('fade_log').style.display = 'block';
}