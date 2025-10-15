// Delete Recipe from favorites
document.querySelectorAll(".recipe-delete").forEach( button => {
    button.addEventListener("click", async e => {
        fetch("/favoriteRecipesRemove", {
            method: "post",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                recipeId: button.id
            })
        })
        .then(res => {
            return res.json();
        })
        .then(json => {
            if(json.answer == "success"){
                button.parentElement.remove();
            }
        })
    });
});