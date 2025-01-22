// Function to add event listener to table
var el = document.getElementById("imgsize");
el.addEventListener("change", function () {
    if (this.selectedIndex === 1) {
        document.querySelector('.custom-size-input').style.display = 'block';
    } else {
        document.querySelector('.custom-size-input').style.display = 'none';
    }
}, false);

var loadFile = function(event) {
    var output = document.getElementById('upload-preview-container');
    output.innerHTML = '';
    for (var i = 0; i < event.target.files.length; i++) {
        var preview = document.createElement("div");
        preview.style = "background-image:url(\'" + URL.createObjectURL(event.target.files[i]) + "\');";
        preview.classList.add('upload-preview');
        output.appendChild(preview);
        preview.onload = function() {
            URL.revokeObjectURL(output.src) // free memory
        }
    }
    document.getElementById('upload_image').submit();
};