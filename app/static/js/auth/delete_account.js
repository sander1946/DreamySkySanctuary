function delete_confirm() {
    fetch('/auth/delete-account', {
        method: 'POST',
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
}