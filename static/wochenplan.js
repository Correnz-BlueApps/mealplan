//Button to remember recipe
async function recipeLike(button) {
    fetch("/favoriteRecipeAdd", {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            recipeId: button.id
        })
    })
    .then(res => {
        return res.json();
    })
    .then(data => {
        console.log("test");
        if (data.answer == "success") {
            button.parentElement.querySelector("a").querySelector(".food-card").classList.add("yellow-transition1")
            setTimeout(() => {
                button.parentElement.querySelector("a").querySelector(".food-card").classList.add("yellow-transition2")
                button.parentElement.querySelector("a").querySelector(".food-card").classList.remove("yellow-transition1")
            }, 600);
            setTimeout(() => {
                button.parentElement.querySelector("a").querySelector(".food-card").classList.remove("yellow-transition2")
            }, 3000);
        }
    })
}


// Button to delete the recipe
function recipeDelete(button) {
    console.log(button);
    button.parentElement.remove();
}

// Button to add one more recipe
document.querySelector("#add-one-recipe").addEventListener("click", async function (e) {        // cannot use arrow function because we want to call "this" later
    fetch("/oneRecipe")
    .then(res => {
        return res.json();
    })
    .then(recipe => {
        const html = `
            <div class="recipe-super-div" id=${ recipe.id }>
                <a href=${ recipe.siteUrl } target="_blank">
                    <div class="food-card">
                        <img src=${ recipe.image } alt="Bild" class="food-img">
                        <div class="food-title">${ recipe.title }</div>
                    </div>
                </a>
                <img onclick="recipeLike(this)" src="/static/star.png" class="recipe-img recipe-star" alt="Like" id=${ recipe.id }>
                <img onclick="recipeDelete(this)" src="/static/delete.png" class="recipe-img recipe-delete" alt="Delete">
            </div>
        `;
        const div = document.createElement("div")
        div.innerHTML = html;
        const newDiv = div.firstElementChild;
    
        // Add and order Element
        const parent = document.querySelector(".recipe-wrapper");
        parent.appendChild(newDiv);
        parent.appendChild(this.parentElement.parentElement);
    });
});

// Button to save Week
document.querySelector("#save-week").addEventListener("click", async function (e) {
    e.preventDefault();
    
    const weekName = document.querySelector("#week-name").value;

    let recipes = [];
    document.querySelectorAll(".recipe-super-div").forEach( recipe => {
        recipes.push(recipe.id);
    });

    if(weekName != ""){
        fetch("/weekAdd", {
        method: "post",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: weekName,
                recipes: recipes
            })
        })
        .then(res => {
            return res.json();
        })
        .then(json => {
            if(json.answer == "success"){
                this.parentElement.parentElement.classList.add("green-transition1")
                setTimeout(() => {
                    this.parentElement.parentElement.classList.add("green-transition2")
                    this.parentElement.parentElement.classList.remove("green-transition1")
                }, 600);
                setTimeout(() => {
                    this.parentElement.parentElement.classList.remove("green-transition2")
                }, 3000);
            }
        });
    }
});