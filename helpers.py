import requests

def recipeById(recipe_id):

    url = f"https://api.chefkoch.de/v2/recipes/{recipe_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return data

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None