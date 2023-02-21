# Functional Specification

## Background:
Our aim is to build a web tool that takes user inputs including user's location, desired category of place the user wants to visit, budget, proximity, etc. and integrates it with the weather conditions to recommend tourist places.

## User Profile:
### 1. Anita:
* Anita is a traveller.
* Anita wants to visit Seattle this summer with her family.
* Anita wants to stay in an area that has interesting activities and places to visit.
* Anita is looking for an all encompassing interface which can provide her relevant information and accounts for Seattle erratic weather.
* Anita does not possess technical skills and she values a simple interface.

### 2. Matt:
* Matt is a technician.
* Matt trains the machine learning model and maintains it.
* Matt needs to ensure that the model is updated as the upstream data (api data) changes.
* Matt observes the hyperparamters and metrics of the model periodically.
* Matt is highly technical and is well versed with the system.

## Data Sources:
This project takes data from two different sources - one for extracting the details of the places close to the user's location, and the other to get the corresponding weather details.
* Place Details API - https://developers.google.com/maps/documentation/places/web-service/details
  - The Place Details request takes in a place_id as parameter (returned from the Place Search API) and returns a response with fields such as: opening_hours, reviews, price_levels, rating, serves_vegetarian_food among others.
* Weather API - https://openweathermap.org/api
  - The Open Weather API call returns current weather data for any location.

## Use Cases:
### 1. Anita:
* Search for interesting activities and places to visit.
* Get recommendations based on real-time weather conditions, proximity and budget.

### Implicit Use Cases:
1. **Recommend the best rated restaurants nearby that serve vegetarian food and are wheelchair friendly**
User: Enters their location, interest(restaurants), specifications(serves vegetarian food and is wheel chair friendly)
Portal: Displays a set of restaurants that follow these specifications

2. **Recommend sightseeing spots to visit in Seattle on a sunny day**
User: Enters their location, interest(sightseeing/tourist spots)
Portal: Displays the top sightseeing spots to visit, when the weather for the specified timings is sunny.

3. **Recommend a list of activities to do on a rainy day in Seattle for children**
User: Enters their location, interest(adventure activities)
Portal: Displays the top activities spots to visit, when the weather for the specified timings is rainy.