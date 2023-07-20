# Tennis Match Scheduler
This Streamlit application helps in scheduling tennis matches. It takes various inputs such as league details, court details, start and end dates, and the number of matches per team to generate a schedule.

# Inputs
League Details: You can input the teams in different leagues. The current setup includes two leagues: "Men's 4.0 Singles" and "Women's 4.0 Singles". Team names are comma-separated.

Start Date: The start date for the schedule.

End Date: The end date for the schedule.

Matches Per Team: The number of matches each team should have within the specified dates.

Court Type: The type of court (options: 3 or 5).

The application currently assumes fixed days for different leagues and fixed court details. The league days and court details are hardcoded in the application, but they can be made flexible based on your needs.

# Outputs
The application generates a schedule for each match with the following details: Teams playing, court location and number, and the date and time of the match.
