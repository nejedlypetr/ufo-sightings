import csv
import calendar
from datetime import datetime

INPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013-raw.csv"
OUTPUT_FILE_PATH = "data/ufo-sightings-usa-1993-2013.csv"

def add_new_headers(reader, writer, new_headers):
    header = next(reader) + new_headers
    writer.writerow(header)

def add_columns(input_file, output_file):
    new_headers = ["Day_of_week", "Month_name", "Day"]
    print("Adding " + str(new_headers) + " columns...")

    with open(input_file, 'r', encoding='utf-8', newline='') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        add_new_headers(reader, writer, new_headers)
        for row in reader:
            datetime = row[1]

            row.append(day_of_week(datetime))
            row.append(month_name(datetime))
            row.append(day_number(datetime))

            writer.writerow(row)

    print(str(new_headers) + " columns added.")

def day_of_week(date_time_str):
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time.strftime('%A')

def month_name(date_time_str):
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return calendar.month_name[date_time.month]

def day_number(date_time_str):
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time.day

if __name__ == "__main__":
    print("Cleaning and preparing data...")
    add_columns(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
    print(f"Output CSV has been created: {OUTPUT_FILE_PATH}")
