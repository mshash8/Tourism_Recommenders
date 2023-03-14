# **ANITA: Weather Integrated Tourism Recommendation System**

# **Project Overview**

[![Coverage Status](https://coveralls.io/repos/github/mshash8/Tourism_Recommenders/badge.svg?branch=main)](https://coveralls.io/github/mshash8/Tourism_Recommenders?branch=main)

## **Introduction**

Our tool takes a user’s inputs including the user’s preference for a particular category of place, date and time of travel, price level, minimum rating and location. The weather can have a significant impact on the types of activities that tourists can engage in at their destination. Thus, the purpose of our system is to enhance the travel experience for tourists by providing them with tailored recommendations that take into account the weather conditions at their destination. For example, if it's raining, the system will suggest indoor activities such as visiting a museum or going to a cafe. If it's sunny, the system will recommend outdoor activities like hiking or visiting a beach.

## **Questions of Interest**

* What are some high end cafes and restaurants I can visit in Seattle two days from now?
* What are some fun outdoor activities to do around me if it is sunny tomorrow?
* Recommend me any tourist activity to do tomorrow appropriate to the weather in Downtown, Seattle
* What are some hikes and trails that I can try two days from now in Olympia based on the weather?

## **Our Goal**

The weather plays a crucial role in tourism, and incorporating weather data into tourism recommendation systems can greatly enhance the usefulness and effectiveness of the recommendations being made. Extreme weather conditions like thunderstorms or heat waves can pose risks to tourists. By incorporating weather data into tourism recommendation systems, these systems can provide recommendations that take into account potential weather-related risks and promote safe and enjoyable travel experiences. Thus, our goal is to provide a valuable service to both tourists and the tourism industry by enhancing the travel experience, promoting tourism, and improving safety.

## **Data Sources**

This project takes data from two different sources - one for extracting the details of the places close to the user's location, and the other to get the corresponding weather details.

### *Google Maps API*

The Google Maps API takes several arguments to including a URL, API key and a 'query' which is based on the category of place and the coordinates of the location. It returns a set of values containing variables like place name, address, photos, opening hours, rating, price level, coordinates, etc.

### *Meteostat Weather API* 

The Meteostat Python library provides a simple API for accessing open weather and climate data. The API returns several variables including the maximum and minimum temperature, cloud coverage, precipitation, wind speed, humidity, etc.
