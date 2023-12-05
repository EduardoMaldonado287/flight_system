import datetime


def dates(start_date, days, weekdays):
    current_date = datetime.date.today()
    days_to_advance = days - (current_date.day - start_date.day)

    for i in range(days_to_advance + 1):
        date = current_date + datetime.timedelta(days=i)
        if date.weekday() in weekdays:
            result_dates.append(date)

    return result_dates


# Example usage

# Get the current date
start_date = datetime.date.today()

# Specify the days of the week
weekdays = [0, 6]  # Monday and Saturday

# Generate the dates
result_dates = dates(start_date, 30, weekdays)

# Print the dates
for date in result_dates:
    print(date)
