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
        });
    });
});

//Delete this week
document.querySelectorAll(".recipe-img-mini").forEach( button => {
    button.addEventListener("click", async e => {
        fetch("/weekRemove", {
            method: "post",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                id: button.id
            })
        })
        .then(res => {
            return res.json();
        })
        .then(data => {
            if(data.answer == "success"){
                button.parentElement.remove();
            }
        });
    });
});