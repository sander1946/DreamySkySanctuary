// Function to add event listener to table
var el = document.getElementById("imgsize");
el.addEventListener("change", function () {
    if (this.selectedIndex === 6) {
        document.querySelector('.custom-size-input').style.display = 'block';
    } else {
        document.querySelector('.custom-size-input').style.display = 'none';
    }
}, false);

var loadFile = function(event) {
    console.log(event)
    console.log(event.target.files)
    var output = document.getElementById('upload-preview-container');
    output.innerHTML = '';
    for (var i = 0; i < event.target.files.length; i++) {
        if (event.target.files[i].size > 80000000) {
            showFlashMessage(event.target.files[i].name + '- File size must be less than 8MB', 'error');
            return;
        }
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