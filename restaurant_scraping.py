import requests
import json

base_url = "https://api.yelp.com/v3/businesses/search?location=Manhattan&term={}%20restaurants&categories=&sort_by=best_match&limit=50&offset={}"

headers = {
    "Authorization": "Bearer aVXvo9S7RwR-5aFHqU_irGLpZySidf-NBw2HE7hOlhGKMSmu-F5un0V0yJqdj1TxmAQ-vt09jcMJG2f5zYzpPu4y5Ie8D7w3C-YADWKHlbTcv-NnCqNBcnqyLN0AZHYx",
    "accept": "application/json"
}

cuisineTypes = ["Chinese", "Greek", "Italian", "Mexican", "Indian", "Thai"] 

for cuisine in cuisineTypes:
    offset = 0
    for i in range(20):
        if offset == 0:
            request_url = base_url.format(cuisine.lower(), offset)
        elif offset == 950:
            request_url = base_url.format(cuisine.lower(), 950)
        else:
            request_url = base_url.format(cuisine.lower(), offset + 1)

        response = requests.get(request_url, headers=headers)

        filename = "restaurants/{}/{}.json".format(cuisine.lower(), i)
        with open(filename, "w") as f:
            json.dump(response.json(), f)

        offset = offset + 50
