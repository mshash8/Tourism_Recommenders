# **ANITA: Weather Integrated Tourism Recommendation System**

# **User Guide**

## **Getting Started**

### *Step 1:*

Open Command Line and clone the project repository to your local system using the following command,
```
>> git clone https://github.com/mshash8/Tourism_Recommenders/tree/main.git
```
### *Step 2:*

To access the project folder, use the ‘cd’ command followed by the path to the directory in which the project folder has been cloned. This would look like,

```
>> cd path/Tourism_Recommenders
```
### *Step 3:*

Initialize the project with the setup.py file using the following command,
```
>> python setup.py install
```
If the above command does not work, try,
```
>> sudo python setup.py install
```
### *Step 4:*

Since this program requires several packages like meteostat, geocoder, geopy, etc. be installed in your local system, run the below command to install all the required packages,

```
>> pip install -r requirements.txt
```
### *Step 5:*

Now that your packages are all installed, you can run the commands below to access the web tool!

```
>> cd Tourism_Recommenders/Tourism_Recommenders
>> streamlit run frontend.py
```

## **Interacting with the Web Tool**
### *Landing Page:*
The landing page looks as follows with several input fields like personal preference, date and time of travel, minimum preferred rating, maximum preferred price level, and location.

![first_image](/examples/images/image1.png)

### *Data Fields:*
The landing page has values filled for most of the variables by default. You can choose a specific value for each of the variables by interacting with them.

1. Personal Preference:

   Choose a preference if any from options like Beaches, Cafes and Restaurants, Hikes and Trails, Indoor Activities, etc. The default value for personal preference is ‘None’.

![second_image](/examples/images/image2.png)

2. Desired Date of Travel:

   Choose your date of travel from the current date to eight days from the current date. Any date before the current date or after eight days from the current date will show an error.

![third_image](/examples/images/image3.png)

3. Desired Time of Travel:

   Choose your desired time of travel from the dropdown menu. Time options are available in intervals of 15 minutes. The default value for time is the current time.

![fourth_image](/examples/images/image4.png)

4. Minimum Preferred Rating:

   Choose the minimum preferred rating you would like for your recommendations. The values range from 1 to 5. The default value for the rating is 3.5.

![fifth_image](/examples/images/image5.png)

5. Maximum Preferred Price Level:

   Choose the maximum preferred price level you would like for your recommendations. The values range from 1 to 5 with 1 being the lowest and 5 the highest. The default value for the price is 3.

![sixth_image](/examples/images/image6.png)

6. Location:

   Enter the location around which you would like your recommendations. The location you enter must be valid and can contain only English letters, digits and commas. If you want the tool to use your current location, leave the field blank. Entering multiple spaces in the field will cause the program to take your current location.

![seventh_image](/examples/images/image7.png)

Once you have entered all the fields, press ‘Enter!’. The program takes around 5-10 seconds to curate a list of recommendations for you!

### *Final Output*

The final output looks as follows! The tool suggests categories of places based on the weather. Since in this case the weather is rainy, it recommends indoor places like cafes, restaurants, museums, etc. If you choose a particular preference, the tool also provides some recommendations pertaining to that. In this case, the preference was set to ‘None’.

![eighth_image](/examples/images/image8.png)

Press the ‘Return’ button on the top left corner to go back to the landing page.

## **Examples**
### *Case 1:*

Assume one of our users, Ellie, is going to Seattle on a business trip tomorrow. She will be staying in Downtown, and would like to visit somewhere (preferably high-end cafes and restaurants) in the evening around 6:30 PM. Ellie can use our Weather Integrated Tourism Recommendation System to get recommendations.
Based on her requirements, she would fill the data fields as follows:

* Personal Preference - Cafes and Restaurants
* Desired Date of Travel - Tomorrow’s date
* Desired Time of Travel - 18:30
* Minimum Preferred Rating - 4.5
* Maximum Preferred Price Level - 5
* Location - Downtown, Seattle

Ellie would not only receive recommendations based on her preference, but also based on the weather. Ellie could then choose to explore other places as well.

### *Case 2:*

Now let’s assume that one of our users, Andrew, has been living in Seattle for the last one year. With Seattle's weather being so erratic, Andrew’s plans don’t always go as planned. Andrew wishes to go explore places around him that are appropriate for that day’s weather. In such a case, Andrew can use our tool to get weather-based recommendations and plan accordingly.
Let’s say Andrew wants to explore places around him at noon, two days from now, with a minimum rating of 3.5 and a minimum budget. Based on his requirements, he would fill the data fields as follows:

* Personal Preference - None
* Desired Date of Travel - Day after tomorrow’s date
* Desired Time of Travel - 12:00
* Minimum Preferred Rating - 3.5
* Maximum Preferred Price Level - 1
* Location - (leave blank to use the current location)

Andrew will then get a list of places he can explore by category based on his desired date’s weather conditions.
