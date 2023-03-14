# Tourism Recommendation Project
[![Coverage Status](https://coveralls.io/repos/github/mshash8/Tourism_Recommenders/badge.svg?branch=main)](https://coveralls.io/github/mshash8/Tourism_Recommenders?branch=main)

## Project Type - Tool
This portal uses user inputs (such as location, time of visit, interest, etc.) and current weather conditions for a location to make recommendations for places to visit.  
## Questions of Interest
* What are the popular places that I can visit in Seattle in June?
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
  - The Open Weather API call returns current weather data for any location.  
