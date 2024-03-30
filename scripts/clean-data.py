import csv
from datetime import datetime

INPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013-raw.csv"
OUTPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013.csv"


def add_day_column(input_file, output_file):
    print("Adding 'Day' column...")

    with open(input_file, 'r', encoding='utf-8', newline='') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header row with the additional 'Day' column
        header = next(reader)
        header.append('Day')
        writer.writerow(header)

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for row in reader:
            date_time_str = row[1] 
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            day_of_week = date_time.weekday()  # Get the day of the week as an integer
            day_name = days[day_of_week] # Map the integer to the corresponding day name

            row.append(day_name)
            writer.writerow(row)
    print("'Day' column added.")

def replace_month_with_name(input_file, output_file):
    print("Replacing 'Month' values with month names...")

    with open(input_file, 'r', encoding='utf-8', newline='') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header row
        header = next(reader)
        writer.writerow(header)

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Augt', 'Sep', 'Oct', 'Nov', 'Dec']

        for row in reader:
            date_time_str = row[1] 
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            month_num = date_time.month  # Get the month as an integer
            month_name = months[month_num - 1]  # Map the integer to the corresponding month name

            row[4] = month_name  # Replace the existing month value with the month name
            writer.writerow(row)
    print("Month names replaced.")


if __name__ == "__main__":
    print("Cleaning data...")
    # add_day_column(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
    # replace_month_with_name(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
    print(f"Output CSV has been created: {OUTPUT_FILE_PATH}")
