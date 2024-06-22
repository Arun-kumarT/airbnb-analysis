# Airbnb-Analysis
This is an open-source project repo which deals with extracting data from Airbnb dataset available in MongoDB Atlas as a sample dataset, pre-processing and loading it into a CSV file for visualization. EDA is done using Streamlit along with Plotly charts and Folium Geospatial Visualization. Also, an interactive dashboard is built using Power BI.

## Introduction
Airbnb, is an American San Francisco-based company operating an online marketplace for short-term and long-term homestays and experiences.  
The company acts as a broker and charges a commission from each booking.  
This project aims at Extracting, Cleaning, Performing the EDA, Visualizing it using Streamlit and Creating an interactive Power BI Dashboard. The dataset is available in the MongoDB Atlas as a Sample Dataset.  

## Table of Contents
1. Pre-requisites
2. Technology Stacks 
3. Usage
4. Data Extraction
5. Data Cleaning and Transformation
6. Visualization and Exploration
7. Dashboard Creation
8. Further Improvements  

## Pre-requsites
Install the following packages to run the project. 
```
pip install streamlit
pip install pandas
pip install folium
pip install streamlit_folium
pip install numpy
pip install sqlalchemy
pip install plotly

```

## Technology Stack
- Python scripting 
- NoSQL - MongoDB Atlas
- Streamlit App development
- Data Pre-processing
- GeoSpatial Visualization
- Plotly
- PowerBI  

## Usage
Clone the repo from the below mentioned link.  
[Airbnb-Analysis](https://github.com/Arun-kumarT/airbnb-analysis.git)   
Install packages from "requirement.txt"  
Run the streamlit application using `streamlit run .\Airbnb.py`      

## Data Extraction 
- Login to the MongoDb Atlas portal  
- Choose "Browse Collections"  
- From the list of collections, select **sample_airbnb.listingsAndReviews**  
- Explore the dataset available  
- To access it from Python, Click the Overview -> Data Toolkit -> App Driver -> Under option 3, you will find the link to access  
- Copy and paste it to Airbnb - Preprocessing.ipynb  
**Note** : Replace your password with <password> in the access link.  

## Data Cleaning and Transformation
- Split the dataset into separate table, so that we can get a clear understanding.
- Handling null values, duplicates and converting the categorical to numerical values (whereever necessary) are performed.
- The following are the important dataframes created.

## Visualization and Exploration
The Exploratory Data Analysis (EDA) is done using Streamlit Application with the help of the below mentioned packages.  
- Folium - GeoSpatial visualization package.  
- Plotly Charts / Plots - Building interactive charts and plots.

## Dashboard Creation
An interactive dashboard with 7+ reports are generated and filtered through a *Country* slicer in Power BI.  
View the dashboard using the link mentioned below.  
[Airbnb-Dashboard](https://github.com/)

## Further Improvements  
The project can further be enhanced by building models to predict the hosts preferences based on seasons and availabilities. This will help us to better understand and recommend to the hosts accordingly.  
If you encounter any issues or have suggestions for improvements, feel free to reach out.  
  
Email : *aarunkumar1797@gmail.com*  
LinkedIn : *https://www.linkedin.com/in/arunkumar-t-8745242ba/*
  
Thanks for showing interest in this repository ! 
