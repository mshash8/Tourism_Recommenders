## Component Specifications

### Component 1 - A frontend module takes in user input and displays information

* Name 
  - index.html
* What it does
  - Hosts the frontend of the tool to take in user inputs and display the requested information.
* Inputs
  - location, user entered location or current location
  - interest, a String that describes what the user is interested in doing(eating at restaurants, activities, etc.)
  - time of visit, A timestamp either entered by the user, or current time
* Output
  - A portal that displays a set of recommendations based on user inputs and specifications
* Assumptions
  - Internet connection and the proper working of the Google places API and openweather API

### Component 2 - Constructing an HTTP request to call the Google places API and the openweather API

* Name
  - getData.py
* What it does
  - Constructs an HTTP request based on user inputs and makes an HTTP call to both the APIs
* Inputs
  - User inputs, a list of the inputs entered by the user
* Outputs
  - The JSON response obtained from the two API calls
* Assumptions
  - Internet connection and the proper working of the Google places API and openweather API

### Component 3 - Parsing the API response text to extract relevant information

* Name
  - textParser.py
* What it does
  - Takes in as input the API responses and extracts relevant information and does text pre-processing
* Inputs
  - The JSON responses from the two HTTP responses
* Outputs
  - A pre-processed text 

### Component 4 - Algorithm to generate recommendations  

* Name
  - generateRec.py
* What it does
  - Takes in the preprocessed information as input and compares it against a set of predefined rules that allow us to make a good recommendation.  
* Inputs  
  - The relevant information from the API responses.  
* Outputs  
  - The recommended tourist spot.

