import csv

relevant_columns = ['id',
                    'host_id',
                    'name',
                    'host_is_superhost',
                    'price',
                    'neighbourhood',
                    'host_name',
                    'neighbourhood_group_cleansed',
                    'review_scores_rating',
                    'beds',
                    'review_scores_rating']

with open("data/listings.csv",
          'r') as source_file,open('data/listings_clean.csv','w',newline='') as cleaned_file:
    reader = csv.DictReader(source_file)
    writer = csv.DictWriter(cleaned_file,
                            fieldnames=[field for field in reader.fieldnames if field in relevant_columns])
    writer.writeheader()
    for row in reader:
        row = {col:row[col] if row[col] != '' else '#NA' for col in relevant_columns}
        writer.writerow(row)
