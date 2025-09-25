import requests

def recipeById(recipe_id):

    url = f"https://api.chefkoch.de/v2/recipes/{recipe_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        
        return {
            "title": data.get("title"),
            "rating": data.get("rating"),
            "hasImage": data.get("hasImage"),
            "prewiewImageUrlTemplate": data.get("prewiewImageUrlTemplate"),
            "fullTags": data.get("fullTags"),
            "ingredients": data.get("ingredientGroups")[0].get("ingredients"),
            "siteUrl": data.get("siteUrl"),
        }

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None