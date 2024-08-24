from datetime import datetime

# Define the date ranges
date_ranges = [
    ("27-Jan-20", "10-Mar-21"),
    ("2-Oct-21", "8-Mar-22"),
    ("14-Jun-22", "7-Oct-22"),
    ("11-Oct-22", "11-Nov-22"),
    ("10-Apr-23", "21-Nov-23"),
    ("10-Apr-24", "10-Sep-24")
]

def calculate_days(start_date, end_date):
    # Convert date strings to datetime objects
    start = datetime.strptime(start_date, "%d-%b-%y")
    end = datetime.strptime(end_date, "%d-%b-%y")
    # Calculate the number of days between the dates (inclusive)
    return (end - start).days + 1

# Calculate and print the number of days for each date range
total_days = 0
for start_date, end_date in date_ranges:
    days = calculate_days(start_date, end_date)
    total_days += days
    print(f"From {start_date} to {end_date}: {days} days")

# Print the total number of days
print(f"Total days calculated: {total_days}")
