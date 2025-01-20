const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
);
const tooltipList = [...tooltipTriggerList].map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const copyToClipboard = async (text, button) => {
    try {
        await navigator.clipboard.writeText(text);
        console.log("Copied to clipboard:", text);
        button.innerHTML =
            "<i class='bi bi-clipboard-check' aria-hidden='true'></i> Copied!";
        button.classList.add("btn-success");
        button.classList.remove("btn-primary");
        setTimeout(() => {
            button.innerHTML =
                "<i class='bi bi-clipboard' aria-hidden='true'></i> Copy Download URL";
            button.classList.add("btn-primary");
            button.classList.remove("btn-success");
        }, 2000);
    } catch (error) {
        console.error("Failed to copy to clipboard:", error);
        // Optional: Handle and display the error to the user
    }
};

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
};