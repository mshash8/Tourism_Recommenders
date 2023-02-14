# Tourism_Recommenders

## Project Type
Tool (Recommendation System).
This tool uses user inputs and interests and combines this with the current weather data for the location to make recommendations for places nearby.  
## Questions of Interest
* What are the top rated restaurants near me? 
* Are there any art museums near me?
* What tourist spots can I visit in Seattle?
* What are the intermediate level hikes that I can try tomorrow? 
## The Goal for the Project Output
A portal that displays set of recommendations based on user inputs, interests and weather conditions.
## The Data Sources
* Place Details API - https://developers.google.com/maps/documentation/places/web-service/details
  - The Place Details request takes in a place_id as parameter (returned from the Place Search API) and returns a response with fields such as: opening_hours, reviews, price_levels, rating, serves_vegetarian_food among others.
* Weather API - https://openweathermap.org/api
  - The open weather API call returns current weather data for any location.  
