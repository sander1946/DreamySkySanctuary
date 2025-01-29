function validate_input(inputfield) {
    if (inputfield.id === 'form') {
        var account = document.getElementById('account');
        var submit = validate_input(account);
        return submit;
    }
    let input = inputfield.value;
    var warning_id = inputfield.id + "_warning";
    var warning = document.getElementById(warning_id);
    var text = "";

    if (input === "") {
        text = "";
    } else if (inputfield.id === 'account') {
        var email_check = new RegExp(".*@.*");
        var emailRegex = new RegExp("..*@..*\\...*");
        var usernameRegex = new RegExp("^[a-zA-Z0-9_]+$");
        if (email_check.test(input)) {
            if (emailRegex.test(input)) {
                text = "";
            } else {
                text = "This is not a valid email address, give a valid email address or an username";
            }
        } else if (!(usernameRegex.test(input) && (input.length <= 32))) {
            text = "Username can only contain letters, numbers, and underscores and must not be longer than 32 characters, give a valid email address or an username";
        } else {
            text = ""
        }
    }

    warning.innerHTML = text;
    if (text === "") {
        warning.style["display"] = "none";
        return true;
    } else {
        warning.style["display"]     = "block";
        return false;
    }
}

const form = document.getElementById('form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const data = new URLSearchParams(new FormData(form));

    const token = document.getElementById('token').value;

    fetch('/auth/reset-password/'+token, {
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
            showFlashMessage('.main-grid', data.detail, data.category);
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});