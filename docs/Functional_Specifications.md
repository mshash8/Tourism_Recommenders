# **ANITA: Weather Integrated Tourism Recommendation System**

# **Functional Specification**

## **Background**

With the development of the tourism industry, several contextual factors such as time, location, and other user preferences are being incorporated into traditional recommender systems in order to increase the prediction accuracy and system utility. However, there is little research on studying the context of weather in tourism recommendation systems. The weather plays a crucial role in tourism, and incorporating weather data into tourism recommendation systems can greatly enhance the usefulness and effectiveness of the recommendations being made. Our aim is to build one such tool that takes user’s inputs including the user’s preference for a particular category of place, date and time of travel, price level, minimum rating and location. The purpose of a weather integrated tourism recommendation system is to enhance the travel experience for tourists by providing them with tailored recommendations that take into account the weather conditions at their destination. For example, if it's raining, the system will suggest indoor activities such as visiting a museum or going to a cafe. If it's sunny, the system will recommend outdoor activities like hiking or visiting a beach. The weather can have a significant impact on the types of activities that tourists can engage in at their destination. Extreme weather conditions like thunderstorms or heat waves can pose risks to tourists. By incorporating weather data into tourism recommendation systems, these systems can provide recommendations that take into account potential weather-related risks and promote safe and enjoyable travel experiences. Thus, our tool can provide a valuable service to both tourists and the tourism industry by enhancing the travel experience, promoting tourism, and improving safety.

## **User Profile**

### *Target Audience*

Our target audience are tourists and travelers who are looking to explore a place and want recommendations based on the weather. For example, independent travelers who are planning their own trip and looking for personalized recommendations can benefit from our tool. Similarly, business travelers who have limited time to explore their destination can benefit from this as well. The system can help them find activities and attractions that are suitable for their schedule. 

### *Level of Computer Experience and Domain Knowledge Needed*

The web tool interface is very simple where the user only needs to input some variables and preferences like price, rating, location, etc. The only requirement from a user is that they preferably be well versed with browsing the web. Since the purpose of our tool is to not challenge our users, the users are not expected to have any prior knowledge in the background of coding. The only thing needed is a stable internet connection for the web tool to run.

### *User Stories*

1. Ellie:
* Ellie is a businesswoman.
* Ellie will be visiting Seattle for a business trip.
* Ellie will be staying in Downtown and she would like to explore some high-end cafes and restaurants in the evening during her free time.
* Ellie has a busy schedule, and is hoping that none of her plans get canceled due to the weather.
* Ellie is looking for an all encompassing interface which can provide her relevant information based on her preferences as well as the weather.

2. Andrew:
* Andrew is a freelancer.
* Andrew has been living in Seattle for the last one year.
* Andrew’s plans however don’t always go as planned due to Seattle’s erratic weather.
* Andrew is looking for a tool to get weather-based recommendations to make plans accordingly.
* Andrew does not possess technical skills and he values a simple interface.

3. Matt:
* Matt is a technician
* Matt maintains the backend code and tries to improve its performance.
* Matt needs to ensure that the tool is up-to-date as the upstream API data changes.
* Matt observes the hyperparameters and metrics of the tool periodically.
* Matt is highly technical and is well-versed with the system.

## **Data Sources**

This project takes data from two different sources - one for extracting the details of the places close to the user's location, and the other to get the corresponding weather details.

### *Google Maps API*

The Google Maps API takes several arguments including a URL, API key and a 'query' which is based on the category of place and the coordinates of the location. It returns a set of values containing variables like place name, address, photos, opening hours, rating, price level, coordinates, etc. The API response is returned as a json object. This data source thus helps us extract real-time data thereby allowing us to provide more accurate recommendations

### *Meteostat Weather API* 

The Meteostat Python library provides a simple API for accessing open weather and climate data. The developers, Meteostat, are an agency that maintain an open source record of global climate data. The historical observations and statistics are collected from different public interfaces, most of which are governmental. Among the data sources are national weather services like the National Oceanic and Atmospheric Administration (NOAA) and Germany's national meteorological service (DWD).

The API returns several variables including the maximum and minimum temperature, cloud coverage, precipitation, wind speed, humidity, etc. The variable of importance for us is the 'coco' value or the Weather Condition Code values. The weather condition codes range from 1 to 27 and represent the weather conditions like clear, sunny, rain, fog, snow, sleet, etc. This variable will allow us to make recommendations based on the weather condition. Since the weather API has data only for the next 8 days from the current date, the desired date of travel for the user cannot exceed these dates.

## **Use Cases**

### *Ellie*

1. Objective:

   Recommend some high-end Cafes and Restaurants in Downtown, Seattle in the evening.

2. User Interaction:
   
   User - Input variables with preference as 'Cafes and Restaurants', desired date of travel, time set to a time in the evening, desired pricing and rating, location as 'Downtown, Seattle'.

   Portal - Recommend places based on the user's preference (in this case Cafes and Restaurants), as well as appropriate places based on the weather.

### *Andrew*

1. Objective:

   Recommend any places to explore around me based on the weather.

2. User Interaction:
   
   User - Input variables with preference as 'None', desired date and time of travel, desired pricing and rating, location as '' to allow the tool to use the current location of the user.

   Portal - Recommend appropriate places by category based on the weather.

### *Implicit Use Cases*

#### 1. User Entered Date and Time Authentication:

* User - Enters the desired date and time of travel in the data fields on the landing page.

* Portal - Authenticates the date and time to ensure that the date is in the future and not beyond 8 days from the current date.
            
   If date is valid, shows recommendations.
            
   If date is invalid, shows an error.
            
 * User - If date is invalid, user clicks the 'Return' button.

 * Portal - Redirects to the landing page.

#### 2. User Input Location Authentication:

 * User - Enters the desired destination's location or leaves blank to allow access to the current location.

 * Portal - If not blank, the program authenticates the location making sure the address is valid and there are no invalid characters.
            
   If location is valid, shows recommendations.
            
   If location is invalid or contains invalid characters, shows an error.
            
 * User - If location is invalid or contains invalid characters, user clicks the 'Return' button.

 * Portal - Redirects to the landing page.
