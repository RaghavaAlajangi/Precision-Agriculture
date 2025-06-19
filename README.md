<h1 align="center">
  Precision-Agriculture app
</h1>



<div align="center">
  <img src="readme_files/app_img.PNG" width="90%">
</div>

## Motivation

* Over the years, technology has reshaped farming, and technical breakthroughs have impacted the agriculture business in a variety of ways.
* Every day, farms generate hundreds of data points about temperature, soil, water usage, weather conditions, and so on. 
* This data is used in real-time with the help of AI and machine learning models to acquire important insights such as predicting the best time to sow seeds, determining crop choices, hybrid seed selection to generate higher yields, and so on.
* AI technologies are assisting in the improvement of overall harvest quality and accuracy — a process known as precision agriculture.

## APP
<https://precision-agriculture.herokuapp.com/>

## Description
* This project is an attempt to make an end-to-end AI application with available agricultural data in the Kaggle website.
* The data has been analyzed and cleaned to create a clean dataset for training.
* Trained the KNN model with the preprocessed dataset, evaluated and tested.
* I used dash API to develop a dashboard and integrated it with the evaluated KNN model to make future crop predictions based on input data.
* You can have a look at how the final dashboard looks like here <https://precision-agriculture.herokuapp.com/>
* As you can see in the dashboard, a user has to enter all the inputs and hit the submit button. As a result, based on the user inputs ML model will predict the crop name in the backend and display the corresponding image.
* It also visualizes the dataset that has been used for training the model both graphically and in tabular form.
* I used the Heroku platform to deploy the application for user interaction.

## Tools used
* Python
* SKlearn
* Dash
* Plotly
