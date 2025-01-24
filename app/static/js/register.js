function validate_input(inputfield) {
    // console.log(inputfield);
    let input = inputfield.value;
    var warning_id = inputfield.id + "_warning";
    var warning = document.getElementById(warning_id);
    // console.log(warning);
    if (input === "") {
        text = "";
    } else if (inputfield.id === 'username') {
        var regex = new RegExp("^[a-zA-Z0-9_]+$");
        if ((regex.test(input)) && (input.length >= 2 && input.length <= 32)) {
            text = "";
        } else {
            text = "Username must be between 2 and 32 characters long and contain only letters, numbers, and underscores";
        }
    } else if (inputfield.id === 'email') {
        var regex = new RegExp(".*@.*\..*");
        if (regex.test(input)) {
            text = "";
        } else {
            text = "This is not a valid email address, it should contain an '@' and an '.'";
        }
    } else if (inputfield.id === 'password') {
        if ((input.length <=32) && (input.length >= 8)) {
            text = "";
        } else {
            text = "Password must be between 8 and 32 characters long";
        }
    } else if (inputfield.id === 'password_rep') {
        if ((input.length <=32) && (input.length >= 8)) {
            if (input === document.getElementById('password').value) {
                text = "";
            } else {
                text = "Passwords do not match";
            }
        } else {
            text = "";
            warning.style.display = "none";
        }
    } else {
        text = "";
    }

    warning.innerHTML = text;
    if (text === "") {
        warning.style["display"] = "none";
    } else {
        warning.style["display"] = "block";
    }
}

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
    var password_rep = document.getElementById("password_rep");
    if (password.type === "password") {
        password.type = "text";
        password_rep.type = "text";
    } else {
        password.type = "password";
        password_rep.type = "password";
    }
}