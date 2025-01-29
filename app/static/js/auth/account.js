const form_username = document.getElementById('change-username');
form_username.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const data = new URLSearchParams(new FormData(form_username));
    console.log(data)
    fetch('/auth/change-username', {
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

const form_email = document.getElementById('change-email');
form_email.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const data = new URLSearchParams(new FormData(form_email));

    fetch('/auth/change-email', {
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

const form_password = document.getElementById('change-password');
form_password.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const data = new URLSearchParams(new FormData(form_password));

    fetch('/auth/change-password', {
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