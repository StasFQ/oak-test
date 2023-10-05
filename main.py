import requests
from abc import ABC, abstractmethod
from pprint import pprint


class RestaurantClient(ABC):

    def __init__(self, user_agent=None):
        self.url = "https://uk.api.just-eat.io/restaurants/bypostcode/"
        self.headers = {
            "User-Agent": user_agent
        }

    @abstractmethod
    def by_postcode(self, postcode):
        pass


class JustEatClientPostCode(RestaurantClient):

    def by_postcode(self, postcode):
        url = self.url + postcode
        print(url)
        try:
            response = requests.get(url, headers=self.headers)

            data = response.json()
            restaurants = []

            for restaurant_data in data.get("Restaurants", []):
                restaurant = {
                    "Name": restaurant_data.get("Name", ""),
                    "Rating": restaurant_data.get("Rating", {}).get("StarRating", 0.0),
                    "Cuisines": [cuisine.get("Name", "") for cuisine in restaurant_data.get("Cuisines", [])]
                }
                restaurants.append(restaurant)

            return restaurants
        except requests.exceptions.RequestException as e:
            raise JustEatClientException("Request failed: " + str(e))


class JustEatClientException(Exception):
    pass


if __name__ == "__main__":
    #If the error occurs, add an user-agent
    user_agent = ""

    client = JustEatClientPostCode(user_agent)
    postcode = "E17DD"

    restaurants = client.by_postcode(postcode)
    pprint(restaurants)
