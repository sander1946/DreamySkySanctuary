function showPassword() {
    var icons = document.getElementsByClassName("password_icon");
    for (var i = 0; i < icons.length; i++) {
        if (icons[i].classList.contains("bi-eye-fill")) {
            icons[i].classList.remove("bi-eye-fill");
            icons[i].classList.add("bi-eye-slash-fill");
        } else {
            icons[i].classList.remove("bi-eye-slash-fill");
            icons[i].classList.add("bi-eye-fill");
        }
    }
    var password = document.getElementById("password");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}