var qrcode = new QRCode(document.getElementById("qrcode"), {
    width : 100,
    height : 100,
    useSVG: true
});

const generate = document.getElementById('generate-otp')
if (generate) {
    generate.onclick = function(event) {
        event.preventDefault();
        fetch('/auth/otp/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        }).then(res => res.json()).then(data => {
            if (data.success) {
                console.log("success");
                console.log(data);
                window.location.reload();
            } else {
                console.log("failed");
                console.log(data);
                showFlashMessage('.fullover-grid', data.detail, data.category);
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    };
}

const verify = document.getElementById('verify-otp')
if (verify) {
    verify.onclick = function(event) {
        event.preventDefault();
        const data = new URLSearchParams(new FormData());
        data.append('token', document.getElementById('token').value)
        console.log(data);

        fetch('/auth/otp/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        }).then(res => res.json()).then(data => {
            if (data.success) {
                console.log("success");
                console.log(data);
                window.location.reload();
            } else {
                console.log("failed");
                console.log(data);
                showFlashMessage('.fullover-grid', data.detail, data.category);
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    };
}

const disable = document.getElementById('disable-otp')
if (disable) {
    disable.onclick = function(event) {
        event.preventDefault();
        const data = new URLSearchParams(new FormData());
        if (document.getElementById('token').value) {
            data.append('token', document.getElementById('token').value)
        } else {
            data.append('token', document.getElementById('token').placeholder)
        }
        
        fetch('/auth/otp/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        }).then(res => res.json()).then(data => {
            if (data.success) {
                console.log("success");
                console.log(data);
                window.location.reload();
            } else {
                console.log("failed");
                console.log(data);
                showFlashMessage('.fullover-grid', data.detail, data.category);
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    };
}

function toggle_fullover() {
    document.getElementById('fullover').classList.toggle('show');
}
