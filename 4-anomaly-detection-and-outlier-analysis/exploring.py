import pandas as pd

# Load the CSV file to inspect its structure and contents
file_path = './4-anomaly-detection-and-outlier-analysis/Data/DATA_FLIGHTID (1).csv'
flight_data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
flight_data.head(), flight_data.info()
