import csv
from geopy.distance import geodesic
from scipy.spatial import KDTree

AIRPORTS_FILE_PATH = "data/public-airports.csv"
UFO_FILE_PATH = "data/ufo-sightings-usa-1993-2013.csv"
OUTPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013-with-public-airports.csv"

def add_new_headers(reader, writer, new_headers):
    header = next(reader) + new_headers
    writer.writerow(header)

def add_airports_data(airports_file, ufo_file, output_file):
    new_headers = ["Nearest_airport", "Nearest_airport_distance"]

    airports = get_list_of_airports(airports_file)
    airport_coords = [coord for _, coord in airports]
    airport_tree = KDTree(airport_coords)

    with open(ufo_file, 'r', encoding='utf-8', newline='') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        add_new_headers(reader, writer, new_headers)
        for row in reader:
            ufo_coords = (float(row[11]), float(row[12]))

            nearest_airport = calculate_shortest_distance_km(ufo_coords, airport_tree, airports)
            row.append(nearest_airport[0])
            row.append(nearest_airport[1])

            writer.writerow(row)

def calculate_shortest_distance_km(ufo_coords, airport_tree, airports):
    # Query the KDTree to find nearest airport
    _, idx = airport_tree.query(ufo_coords)
    
    nearest_airport = airports[idx]
    nearest_airport_name = nearest_airport[0]
    nearest_airport_coords = nearest_airport[1]
   
    # Calculate the geodesic distance in kilometers
    distance = geodesic(ufo_coords, nearest_airport_coords).kilometers
    shortest_distance = round(distance, 2)

    return nearest_airport_name, shortest_distance

def get_list_of_airports(airports_file):
    with open(airports_file, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        next(reader) # skip headers
        
        airports = []
        for row in reader:
            name = row[1]
            coord = (float(row[5]), float(row[6]))
            airports.append((name, coord))
        
        return airports

if __name__ == "__main__":
    print("Adding airports data...")
    add_airports_data(AIRPORTS_FILE_PATH, UFO_FILE_PATH, OUTPUT_FILE_PATH)
    print(f"Output CSV has been created: {OUTPUT_FILE_PATH}")
