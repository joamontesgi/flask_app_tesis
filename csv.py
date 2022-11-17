import csv
data = ["This", "is", "a", "Test"]
with open('example.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(data)

