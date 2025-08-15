# Bengaluru House Price Predictor

This project provides two different interfaces for predicting house prices in Bengaluru using machine learning:

1. **Flask Web Application** (`main.py`)
2. **Streamlit Application** (`streamlit_app.py`)

## Streamlit App Screenshots

All images show different features of the Streamlit application:

| Main Interface | Market Insights |
|----------------|----------------|
| ![Main Interface](image1.png) | ![Market Insights](image2.png) |

| Top Expensive Areas | Price Analysis |
|-------------------|----------------|
| ![Top Expensive Areas](image3.png) | ![Price Analysis](image4.png) |


## Features

- 🏠 Predict house prices based on location, BHK, bathrooms, and square footage
- 📊 Market insights and statistics for different areas
- 🎯 Real-time price predictions using Ridge Regression model
- 📈 Price analysis and breakdowns
- 🏆 Top expensive areas ranking

## Prerequisites

Make sure you have the following files in your project directory:
- `Cleaned_data.csv` - The cleaned housing dataset
- `RidgeModel.pki` - The trained Ridge Regression model

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Applications

### Option 1: Streamlit Application (Recommended)

The Streamlit version provides a more modern and interactive interface with additional features:

```bash
streamlit run streamlit_app.py
```

**Features of Streamlit App:**
- Interactive widgets and real-time updates
- Market insights for selected locations
- Price distribution charts
- Sidebar with dataset information
- Top expensive areas ranking
- Price per sq ft, BHK, and bathroom analysis

### Option 2: Flask Web Application

The traditional Flask web application:

```bash
python main.py
```

Then open your browser and go to: `http://localhost:5001`

## Usage

1. **Select Location**: Choose the area/location of the property
2. **Enter BHK**: Number of Bedrooms, Hall, and Kitchen
3. **Number of Bathrooms**: Total bathrooms in the property
4. **Square Feet**: Total area of the property
5. **Predict**: Click the predict button to get the estimated price

## Model Information

- **Algorithm**: Ridge Regression
- **Features**: Location, Total Square Feet, Bathrooms, BHK
- **Output**: Price prediction in Indian Rupees (₹)

## File Structure

```
Bengaluru housing data/
├── main.py              # Flask application
├── streamlit_app.py     # Streamlit application
├── RidgeModel.pki       # Trained model
├── Cleaned_data.csv     # Dataset
├── templates/
│   └── index.html       # Flask template
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Technologies Used

- **Backend**: Python, Flask, Streamlit
- **Machine Learning**: Scikit-learn, Ridge Regression
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, CSS, Bootstrap (Flask), Streamlit Components

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the UI/UX
- Optimizing the model
- Adding more data analysis capabilities

## License

This project is open source and available under the MIT License.
