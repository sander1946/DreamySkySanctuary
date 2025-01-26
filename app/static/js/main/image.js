const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const copyToClipboard = async (input_id, button) => {
    var input_code = document.getElementById(input_id);
    var text = input_code.value
    var innerHtml = button.innerHTML;
    try {
        await navigator.clipboard.writeText(text);
        console.log("Copied to clipboard:", text);
        button.innerHTML =
            "<i class='bi bi-clipboard-check' aria-hidden='true'></i>";
        button.classList.add("btn-success");
        button.classList.remove("btn-primary");
        setTimeout(() => {
            button.innerHTML = innerHtml;
            button.classList.add("btn-primary");
            button.classList.remove("btn-success");
        }, 2000);
    } catch (error) {
        console.error("Failed to copy to clipboard:", error);
        // Optional: Handle and display the error to the user
    }
};