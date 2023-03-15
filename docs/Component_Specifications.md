## Component Specifications

### Component 1 - Frontend Module

* What it does
  - This module takes in information based on user preferences which are entered using text boxes and drop down menus. These user inputs are then used in order to generate recommendations for the best things for the user to do on that day which is displayed to the user along with the weather at that point. Two types of  recommendations are generated, one  based on the input as well as one based on the weather for that particular day. 
* Inputs
  - User entered location or current location
  - interest, a String that describes what the user is interested in doing(eating at restaurants, activities, etc.)
  - time of visit, A timestamp either entered by the user, or current time
  - Date of visit, or current day
  - Maximum price range, scale of 1-5
  - Minimum rating, scale of 1-5
* Output
  - What the weather is on the specified day at the specified time, the recommended activities/ places to visit.  
* Assumptions
  - Internet connection and the proper working of the Google places API and openweather API

### Component 2 -  Google Maps API Module

* What it does
  - This module constructs the GET request to the google maps API based on the user input and the pre-defined search queries. It then calls the google maps API and returns the results.
* Inputs
  - The Maps API URL
  - List of queries to be searched
  - The decoded API key
  - Any optional fields
  - Latitude of location
  - Longitude of location
  - Minimum rating of the recommendation
  - Maximum price level of the recommendation
* Outputs
  - The filtered and sorted dataframe containing the list of recommendations
* Assumptions
  - Internet connection and the proper working of the Google places API and openweather API

### Component 3 - Weather Condition Module

* What it does
  - Fetches hourly weather data from nearby weather stations. It then extracts the weather condition codes. Finally, the average of these codes are computed to give the weather condition code.
* Inputs
  - Latitude of location
  - Longitude of location
  - Date of visit
  - Time of visit
* Outputs
  - The predicted average hourly weather condition.

### Component 4 - Visit Location Module

* What it does
  - Finds the latitude and longitude values of the location that the user enters. However, if the location input is left blank, then the latitude and longitude of the user’s current location is obtained.  
* Inputs  
  - Location input from user or user’s current location 
* Outputs  
  - The latitude and the longitude of the input location

### Component 5 - Rules Module
* What it does 
  This function curates a list of search queries based on the following rules:
  - A weather condition code equal to zero means that the weather for that day is uncertain. In such a case, recommendations are made across all categories without taking weather into consideration. 
  - A weather condition code <= 2 denotes a clear and sunny day. In such cases, beaches, parks, hikes, etc. are recommended. 
  - A weather condition  code >2 and <= 5 denotes a cloudy day. In such case, cafes, hikes, musuems, etc. are recommended. 
  - A weather condition code >5 and <= 11, or equal to 17 or 18 signifies  a rainy day. In such case, cafes, musuems, indoor activities etc. are recommended. 
  - A weather condition code equal to 14, 15 or 21 implies a snowy day. In such cases, cafes, snow hikes, restaurants, etc. are recommended. 
  - For any other value, the weather is not favourable to go out, and thus no recommendations are made.
* Inputs 
  - Average hourly weather condition for the user's preferred date and time
  - User’s location
* Outputs 
  - a list of search queries which allow the Google Maps API to fetch data.

## Use Case
Case: User wants recommendations for activities in Seattle on 16th March 2023. 
The user inputs the date of their visit, time, maximum price, minimum rating, preference of activity and location into the Frontend Module. If the user does not input their location, the location module will locate their current location. The Location module returns the latitude and longitude of the location which the Meteostat API module takes as input along with date and time in order to return the weather conditions as a code. This information is then sent to the Basic Rules Module which constructs a list of queries to be sent to the Google Maps API module which returns the recommendations which are displayed to the user.


## Preliminary plan(Milestones) - A list of tasks in priority order.

### Week 1 (14th-21st February, 2023)
* Create a comprehensive docs folder with functional specifications and component specifications.
* Discover packages that work for our use case and perform a comparison analsis
* Ensure that the packages that are being used work efficiently and document any downfalls
* Develop the tests to confirm the expected working of the components (test driven development)

### Week 2 (21st-28th February, 2023)
* Develop the tests to confirm the expected working of the components (test driven development)
* Develop the components for the web application
* Ensure that the frontend and backend of the application are in connected 

### Week 3 (28th February-7th March, 2023)
* Develop the components for the web application
* Conduct user acceptance and end-to-end testing


### Week 4 (7th-14th March, 2023)
* Revisions and changes based on feedback from peers and instructors
