function showFlashMessage(message, category) {
    var main_grid = document.querySelector('.main-grid');
    var flash = document.createElement("div");
    flash.classList.add("flash-"+category, "bg-glass", "text-center");
    flash.innerHTML = message;
    main_grid.insertBefore(flash, main_grid.firstChild);
    setTimeout(function() {
        flash.remove();
    }, 5000);
}