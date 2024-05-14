import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
from scipy.spatial import cKDTree
from geopy.distance import geodesic


DATA_FILE_PATH = "data/ufo-sightings-usa-1993-2013-with-public-airports.csv"
PUBLIC_AIRPORTS_FILE_PATH = "data/public-airports.csv"
US_STATES_TERRITORIES_PATH = "data/us-states-territories.csv"


def plot_ufo_airport_correlation(csv_file):
    data = pd.read_csv(csv_file)
    data['Nearest_airport_distance'] = data['Nearest_airport_distance'].round()

    # Group the data by nearest airport distance and count the number of sightings in each distance category
    sightings_by_distance = data.groupby('Nearest_airport_distance').size().reset_index(name='Num_Sightings')

    # Remove outliers beyond a certain threshold distance
    threshold_distance = 100
    sightings_by_distance = sightings_by_distance[sightings_by_distance['Nearest_airport_distance'] <= threshold_distance]

    # Calculate the correlation coefficient
    correlation_coefficient = sightings_by_distance['Num_Sightings'].corr(sightings_by_distance['Nearest_airport_distance'])
    print("Correlation coefficient:", correlation_coefficient)

    # Plot the correlation graph
    plt.figure(figsize=(10, 6))
    plt.scatter(sightings_by_distance['Nearest_airport_distance'], sightings_by_distance['Num_Sightings'])
    plt.xlabel('Distance of Nearest Airport (km)')
    plt.ylabel('Number of UFO Sightings')
    plt.title('Correlation between UFO Sightings and Nearest Airport Distance')
    plt.grid(True)
    plt.show()

    #### SAVE a color adjusted graph
    # plt.figure(figsize=(10, 6))
    # plt.scatter(sightings_by_distance['Nearest_airport_distance'], sightings_by_distance['Num_Sightings'], color='#5B54A1')
    # plt.grid(True, color='white')
    # plt.gca().spines['top'].set_color('white')
    # plt.gca().spines['bottom'].set_color('white')
    # plt.gca().spines['left'].set_color('white')
    # plt.gca().spines['right'].set_color('white')
    # plt.gca().tick_params(axis='x', colors='white', labelsize=12)
    # plt.gca().tick_params(axis='y', colors='white', labelsize=12)
    # plt.savefig('ufo_airport_data_distribution.png', transparent=True) # Save the plot with a transparent background
    
def plot_ufo_airport_correlation_log(csv_file):
    data = pd.read_csv(csv_file)
    data['Nearest_airport_distance'] = data['Nearest_airport_distance'].round()

    # Group the data by nearest airport distance and count the number of sightings in each distance category
    sightings_by_distance = data.groupby('Nearest_airport_distance').size().reset_index(name='Num_Sightings')

    # Remove outliers beyond a certain threshold distance
    threshold_distance = 100
    sightings_by_distance = sightings_by_distance[sightings_by_distance['Nearest_airport_distance'] <= threshold_distance]

    # Calculate the correlation coefficient
    correlation_coefficient = sightings_by_distance['Num_Sightings'].corr(sightings_by_distance['Nearest_airport_distance'])
    print("Correlation coefficient:", correlation_coefficient)

    # Perform linear regression after taking the logarithm of y-values
    x = sightings_by_distance['Nearest_airport_distance']
    y = sightings_by_distance['Num_Sightings']
    y_log = np.log(y)

    slope, intercept, r_value, p_value, std_err = linregress(x, y_log)

    # Plot the correlation graph
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label='Data')
    plt.plot(x, np.exp(intercept + slope * x), color='red', label='Line of Best Fit')  # Exponentiate the linear regression line to transform it back
    plt.xlabel('Distance of Nearest Airport (km)')
    plt.ylabel('Number of UFO Sightings')
    plt.title('Correlation between UFO Sightings and Nearest Airport Distance')
    plt.grid(True)
    plt.yscale('log')
    plt.legend()
    plt.show()

    #### SAVE a color adjusted graph
    # plt.figure(figsize=(10, 6))
    # plt.scatter(x, y, label='Data', color='#5B54A1')
    # plt.plot(x, np.exp(intercept + slope * x), color='red', label='Line of Best Fit')
    # plt.grid(True, color='white')
    # plt.yscale('log')
    # plt.legend()
    # plt.gca().spines['top'].set_color('white')
    # plt.gca().spines['bottom'].set_color('white')
    # plt.gca().spines['left'].set_color('white')
    # plt.gca().spines['right'].set_color('white')
    # plt.gca().tick_params(axis='x', colors='white', labelsize=12)
    # plt.gca().tick_params(axis='y', colors='white', labelsize=12)
    # plt.savefig('ufo_airport_data_distribution_log.png', transparent=True) # Save the plot with a transparent background

def calculate_percentage_of_sightings_within_distance(csv_file):
    df = pd.read_csv(csv_file)

    # Convert Nearest_airport_distance to numeric
    df['Nearest_airport_distance'] = pd.to_numeric(df['Nearest_airport_distance'], errors='coerce')
    df = df.dropna(subset=['Nearest_airport_distance']) # Filter out rows with missing distances

    total_sightings = df.shape[0]

    within_range = df[(df['Nearest_airport_distance'] >= 5) & (df['Nearest_airport_distance'] <= 10)].shape[0]
    within_5_km = df[df['Nearest_airport_distance'] <= 5].shape[0]
    within_10_km = df[df['Nearest_airport_distance'] <= 10].shape[0]
    within_15_km = df[df['Nearest_airport_distance'] <= 15].shape[0]

    # Calculate percentages
    percentage_within_range = (within_range / total_sightings) * 100
    percentage_within_5_km = (within_5_km / total_sightings) * 100
    percentage_within_10_km = (within_10_km / total_sightings) * 100
    percentage_within_15_km = (within_15_km / total_sightings) * 100

    return {
        'Within 5 to 10 km': percentage_within_range,
        'Within 5 km': percentage_within_5_km,
        'Within 10 km': percentage_within_10_km,
        'Within 15 km': percentage_within_15_km
    }

def calculate_sightings_per_km2(dataset_path, state_data_path):
    ufo_data = pd.read_csv(dataset_path)

    # Read state data
    state_data = pd.read_csv(state_data_path, encoding='ISO-8859-1')

    # Strip whitespace from relevant columns
    state_data['Name'] = state_data['Name'].str.strip()
    ufo_data['Region'] = ufo_data['Region'].str.strip()

    # Merge datasets on state name
    merged_data = pd.merge(ufo_data, state_data, left_on="Region", right_on="Name", how="inner")

    # Convert area from square miles to square kilometers
    merged_data['area (square miles)'] = pd.to_numeric(merged_data['area (square miles)'], errors='coerce')
    merged_data['area (square km)'] = merged_data['area (square miles)'] * 2.58999

    # Group the data by state and count sightings
    sightings_per_state = merged_data.groupby("Name").size()

    # Calculate sightings per 100 km² for each state
    sightings_per_100km2 = (sightings_per_state / merged_data.groupby("Name")['area (square km)'].mean()) * 100

    # Sort the result by the highest number of sightings per 100 km²
    sightings_per_100km2_sorted = sightings_per_100km2.sort_values(ascending=False)

    return sightings_per_100km2_sorted


if __name__ == "__main__":
    print("Data analysis...\n")

    # print("Percentage of sightings within distance:")
    # print(calculate_percentage_of_sightings_within_distance(DATA_FILE_PATH))

    # sightings_per_km2 = calculate_sightings_per_km2(DATA_FILE_PATH, US_STATES_TERRITORIES_PATH)
    # print("Sightings per 100 km²:")
    # print(sightings_per_km2)

    # plot_ufo_airport_correlation(PUBLIC_AIRPORTS_FILE_PATH)
    # plot_ufo_airport_correlation_log(PUBLIC_AIRPORTS_FILE_PATH)
