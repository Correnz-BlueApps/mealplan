import requests

def recipeById(recipe_id):
    url = f"https://api.chefkoch.de/v2/recipes/{recipe_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None