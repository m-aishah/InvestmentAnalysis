import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Data dictionary for each location
data = {
    "Date": [
        "Thu Mar 01 2018", "Fri Jun 01 2018", "Sat Sep 01 2018", "Sat Dec 01 2018",
        "Fri Mar 01 2019", "Sat Jun 01 2019", "Sun Sep 01 2019", "Sun Dec 01 2019",
        "Sun Mar 01 2020", "Mon Jun 01 2020", "Tue Sep 01 2020", "Tue Dec 01 2020",
        "Mon Mar 01 2021", "Tue Jun 01 2021", "Wed Sep 01 2021", "Wed Dec 01 2021",
        "Tue Mar 01 2022", "Wed Jun 01 2022", "Thu Sep 01 2022", "Thu Dec 01 2022",
        "Wed Mar 01 2023", "Thu Jun 01 2023", "Fri Sep 01 2023", "Fri Dec 01 2023",
        "Fri Mar 01 2024"
    ],
    "Girne": [
        924.39, 916.77, 875.21, 861.9, 841.44, 816.22, 803.87, 796.26, 795.46,
        774.25, 754.16, 736.32, 745.78, 760.45, 762.87, 790.64, 777.27, 852.04,
        930.58, 1039.58, 1157.71, 1277.3, 1350.69, 1426.58, 1433.5
    ],
    "Kyrenia": [
        851.37, 825.29, 795.2, 757.06, 755.29, 781.18, 789.98, 761.77, 773.54,
        728.91, 699.31, 699.76, 708.61, 711.99, 747.71, 761.93, 742.21, 816.89,
        846.69, 946.34, 1057.6, 1154.47, 1286.34, 1423.4, 1536.51
    ],
    "Iskele": [
        813.05, 795.18, 787.32, 790.87, 808.76, 846.73, 881.24, 908.83, 925.76,
        977.77, 964.36, 942.36, 969.6, 974.05, 977.66, 1009.87, 1075.29, 1073.66,
        1169.73, 1284.12, 1431.34, 1591.48, 1771.35, 1826.04, 1910.6
    ],
    "Gonyeli": [
        584.98, 568.06, 559.21, 548.08, 534.4, 535.47, 534.93, 541.04, 543.19,
        531.93, 524.1, 523.14, 514.89, 503.8, 519.54, 510.76, 503.03, 478.93,
        496.84, 535.5, 589.92, 647.54, 707.59, 769.86, 838.87
    ],
    "Lefkosa": [
        570.02, 562.53, 569.51, 550.78, 542.73, 544.28, 539.87, 544.02, 545.67,
        528.85, 511.74, 494.07, 488.13, 494.42, 503.18, 502.92, 526.49, 512.62,
        555.99, 583.4, 625.84, 681.46, 702.22, 701.24, 769.03
    ],
    "Famagusta": [
        603.79, 604.8, 587.39, 574.77, 549.96, 529.21, 540.53, 539.96, 521.77,
        503.54, 503.95, 506.05, 511.54, 530.15, 514.92, 537.11, 523.61, 580.87,
        633.82, 672.17, 750.76, 838, 925.43, 1017.65, 1069.35
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)
# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Function to calculate Compound Annual Growth Rate (CAGR)
def calculate_cagr(initial_price, final_price, years):
    cagr = (final_price / initial_price) ** (1 / years) - 1
    return cagr

# Function to fit a linear regression model and predict future prices
def predict_future_prices(df, location, years_ahead):
    # Convert dates to ordinal numbers for regression
    df["OrdinalDate"] = df["Date"].map(lambda x: x.toordinal())
    
    # Fit linear regression model
    X = df["OrdinalDate"].values.reshape(-1, 1)
    y = df[location].values
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future prices
    future_dates = pd.date_range(start=df["Date"].iloc[-1], periods=years_ahead + 1, freq='YS')
    future_dates_ordinal = future_dates.map(lambda x: x.toordinal()).values.reshape(-1, 1)
    future_prices = model.predict(future_dates_ordinal)
    
    return future_dates, future_prices

# Function to calculate expected return per square meter using regression
def calculate_expected_return_per_sqm(df, location, years_ahead=5):
    future_dates, future_prices = predict_future_prices(df, location, years_ahead)
    
    # Calculate the average annual return over the specified number of years
    initial_price = df[location].iloc[-1]
    final_price = future_prices[-1]
    years = years_ahead
    cagr = calculate_cagr(initial_price, final_price, years)
    expected_return_per_sqm = cagr * 100  # as a percentage
    
    return expected_return_per_sqm

# Function to estimate potential revenue using predicted prices
def estimate_potential_revenue(df, location, property_size, years_ahead):
    _, future_prices = predict_future_prices(df, location, years_ahead)
    
    # Estimate the price per square meter after the specified number of years
    estimated_price_per_sqm = future_prices[-1]
    
    # Potential revenue
    potential_revenue = estimated_price_per_sqm * property_size
    
    return potential_revenue

# Function to display information for a specific location
def display_location_information(df, location, years_ahead, property_size):
    if location in df.columns:
        expected_return_per_sqm = calculate_expected_return_per_sqm(df, location, years_ahead)
        potential_revenue = estimate_potential_revenue(df, location, property_size, years_ahead)
        
        # Print results
        print(f"{location} - Expected Return per sqm: {expected_return_per_sqm:.2f}%")
        print(f"Potential Revenue for {property_size} sqm in {location} over {years_ahead} years: ${potential_revenue:,.2f}")

# Example usage
property_size = 100  # square meters
years_ahead = 5  # Number of years in the future
location_to_display = "Gonyeli"  # Replace with the location you want to display

# Display information for the specified location
display_location_information(df, location_to_display, years_ahead, property_size)
