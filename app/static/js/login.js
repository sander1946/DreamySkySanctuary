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

const form = document.getElementById('form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const data = new URLSearchParams(new FormData(form));

    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data
    }).then(res => res.json()).then(data => {
        if (data.success) {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } else {
            showFlashMessage(data.detail, data.category);
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});