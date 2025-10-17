//Button to remember recipe
document.querySelectorAll(".recipe-star").forEach( button => {
    button.addEventListener("click", async e => {
        const res = await fetch("/favoriteRecipeAdd", {
            method: "post",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                recipeId: button.id
            })
        });
        if (res == "0") {
            console.log("test");
        }
    });
});


// Button to delete the recipe
document.querySelectorAll(".recipe-delete").forEach( button => {
    button.addEventListener("click", e => {
        button.parentElement.remove();
    });
});

// Button to add one more recipe
document.querySelector("#add-one-recipe").addEventListener("click", async function (e) {        // cannot use arrow function because we want to call "this" later
    fetch("/oneRecipe")
    .then(res => {
        return res.json();
    })
    .then(recipe => {
        const html = `
            <div class="recipe-super-div">
                <a href=${ recipe.siteUrl } target="_blank">
                    <div class="food-card">
                        <img src=${ recipe.image } alt="Bild" class="food-img">
                        <div class="food-title">${ recipe.title }</div>
                    </div>
                </a>
                <img src="/static/star.png" class="recipe-img recipe-star" alt="Like" id=${ recipe.id }>
                <img src="/static/delete.png" class="recipe-img recipe-delete" alt="Delete">
            </div>
        `;
        const div = document.createElement("div")
        div.innerHTML = html;
        const newDiv = div.firstElementChild;
    
        // Add and order Element
        const parent =document.querySelector(".recipe-wrapper");
        parent.appendChild(newDiv);
        parent.appendChild(this.parentElement);
    });
});

// Button to save Week
document.querySelector("#save-week").addEventListener("click", async e => {
    const weekName = document.querySelector("#week-name").value;
    if(weekName != ""){
        fetch("/saveWeek", {
        method: "post",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: weekName
            })
        })
        .then(res => {
            return res.json();
        })
        .then(json => {
            if(json == "success"){
                console.log("recipe week saved")
            }
        });
    }
});