// Button to delete the recipe
document.querySelectorAll(".recipe-delete").forEach( button => {
    button.addEventListener("click", e => {
        button.parentElement.remove();
    });
});