Bengaluru House Price Prediction

This project focuses on predicting house prices in Bengaluru using a machine learning regression model.
The goal is to estimate property prices based on inputs like location, total square footage, number of bedrooms (BHK), and number of bathrooms. 
The model is trained on a real-world housing dataset and includes data preprocessing steps, feature engineering, and model evaluation. 
An optional Flask-based web application allows users to input details and get instant price predictions.

![Output](https://github.com/gagandeep1763/Bengaluru_house_data_prediction/raw/main/output%201.png)

Overview
The primary aim of this project is to create a machine learning model that can accurately predict housing prices. 
It involves cleaning raw data, engineering features, handling outliers, and training a regression model.
The project also includes an optional web interface to interact with the model.

Key Objectives:
Clean and preprocess the dataset.
Handle missing and inconsistent values.
Perform feature engineering (like extracting BHK from size).
Remove outliers using domain-specific logic.
Encode categorical features like location.
Build and train a regression model.
Evaluate performance using metrics like R² score.
Deploy using a simple web interface (Flask).

Features
Dataset cleaning and null value handling.
Size and price per square foot calculations.
One-hot encoding for categorical data.
Outlier detection and removal based on area per BHK and price per sqft.
Ridge regression model for prediction.
Simple web interface using Flask (optional).

Dataset

The dataset contains housing listings from Bengaluru and includes the following fields:

Location.

Size (converted to BHK).

Total Square Feet.

Number of Bathrooms.

Price (in lakhs).

The dataset was originally sourced from Kaggle and filtered for this project.

Technologies Used : 

Python,
Pandas, NumPy (data analysis and manipulation),
Scikit-learn (machine learning),
Jupyter Notebook (development and visualization),
Flask (for building the web app interface)

How to Run:

Clone the repository.

Open and run the Jupyter Notebook (House_price.ipynb) to preprocess data and train the model.

The model is saved using Pickle as RidgeModel.pki.

To run the web app:

Make sure Flask is installed (pip install flask).
Run main.py    .

Open http://localhost:5000 in your browser. 

Enter inputs like location, sqft, BHK, and bathroom count to get predicted price.

Folder Structure:
Bengaluru_House_Data.csv – Raw housing dataset .
Cleaned_data.csv – Processed data after cleaning .
House_price.ipynb – Jupyter Notebook for development and training .
RidgeModel.pki – Saved trained model using Pickle .
main.py – Flask backend for prediction interface .
templates/ – HTML templates for Flask UI .
static/ – Optional folder for CSS and JS files (if used) .

Model Details
Model used: Ridge Regression.

Preprocessing: One-hot encoding, StandardScaler.

R² Score: 0.87 on test data.

Pipeline: Combined preprocessing and model training in a single pipeline.

Future Improvements:
Try more advanced models like Random Forest or XGBoost.

Add budget-based recommendations.

Integrate with live property APIs.

Host the app on platforms like Heroku, Render, or AWS.

Developed By

Gagandeep D

Google Certified UI/UX Designer
