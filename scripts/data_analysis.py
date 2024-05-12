import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress

PUBLIC_AIRPORTS_FILE_PATH = "data/ufo-sightings-usa-1993-2013-with-public-airports.csv"


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

# todo: calculate average distance between airports

# todo: calculate percatage of how many sightings appeared within 5, 10, 15 km from an airport

# todo: calculate sightings of city per area (km)


if __name__ == "__main__":
    print("Data analysis...")

    plot_ufo_airport_correlation(PUBLIC_AIRPORTS_FILE_PATH)
    plot_ufo_airport_correlation_log(PUBLIC_AIRPORTS_FILE_PATH)
