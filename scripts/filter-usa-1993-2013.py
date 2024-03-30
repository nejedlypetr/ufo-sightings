import csv

INPUT_FILE_PATH = "data/ufo-sightings-raw.csv"
OUTPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013-raw.csv"


def filter_csv(input_file, output_file):
    print("Filter script running...")
    
    with open(input_file, 'r', encoding='utf-8', newline='',) as infile, open(output_file, 'w', encoding='utf-8', newline='',) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header row
        header = next(reader)
        writer.writerow(header)

        id_counter = 0
        for row in reader:
            # Check if the country is USA and the year is between 1993 and 2013
            if row[7] == 'USA' and 1993 <= int(row[3]) <= 2013:
                row[0] = id_counter
                writer.writerow(row)
                id_counter += 1
    
    print(f"Filtered CSV has been created: {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    filter_csv(INPUT_FILE_PATH, OUTPUT_FILE_PATH)