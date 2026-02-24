import calendar

# Input: month day year
month, day, year = map(int, input().split())

# Get weekday number
day_number = calendar.weekday(year, month, day)

# Get day name
day_name = calendar.day_name[day_number].upper()

# Get month name
month_name = calendar.month_name[month]

# Print formatted output
print(day_name)
print(f"The day on {month_name} {day} was {day_name}.")