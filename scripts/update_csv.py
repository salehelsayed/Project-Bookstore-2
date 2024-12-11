import csv
import random

# Read the CSV file
csv_file = 'c:/Users/s/Desktop/Windsurf-output/Project-bookstore-2/data/books_data.csv'
rows = []

with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Get the header row
    rows.append(header)
    
    # Process each row
    for row in csv_reader:
        # Add random values for top_downloads and most_discussed
        if len(row) > 12:  # Make sure we have the base columns
            # Generate random numbers between 10 and 150
            top_downloads = random.randint(10, 150)
            most_discussed = random.randint(10, 150)
            
            # If the row already has these columns, update them
            if len(row) >= 14:
                row[-2] = str(top_downloads)
                row[-1] = str(most_discussed)
            else:
                # If not, append them
                row.extend([str(top_downloads), str(most_discussed)])
        rows.append(row)

# Write back to the CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(rows)

print("CSV file has been updated with random values for top_downloads and most_discussed.")
