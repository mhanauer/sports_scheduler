import streamlit as st
import pandas as pd
import itertools
import random
from datetime import datetime, timedelta
import holidays

def generate_dates(start_date, end_date, day_of_week):
    us_holidays = holidays.US(years=[start_date.year, end_date.year])
    holiday_weeks = [date.isocalendar()[1] for date in us_holidays]
    dates = []
    total_days = (end_date - start_date).days + 1
    for day_number in range(total_days):
        current_day = start_date + timedelta(days=day_number)
        if current_day.weekday() == day_of_week and current_day.isocalendar()[1] not in holiday_weeks:
            dates.append(current_day)
    return dates

def schedule_matches(leagues, league_days, court_details, start_date, end_date, weekday_times, weekend_times, matches_per_team, court_type):
    schedules = {league: list(itertools.combinations(teams, 2)) for league, teams in leagues.items()}
    for schedule in schedules.values():
        random.shuffle(schedule)

    weekday_times = [datetime.strptime(time, "%I:%M %p") for time in weekday_times]
    weekend_times = [datetime.strptime(time, "%I:%M %p") for time in weekend_times]
    
    league_dates = {league: [] for league in leagues}
    for league, days_of_week in league_days.items():
        for day_of_week in days_of_week:
            league_dates[league].extend(generate_dates(start_date, end_date, day_of_week))
    
    court_slots = [(location, list(court_numbers[i:i+court_type])) for location, court_numbers in court_details.items() for i in range(0, len(court_numbers), court_type)]
    
    league_date_time_slots = {league: [datetime.combine(date, time.time()) if date.weekday() < 5 else datetime.combine(date, time.time()) for date in league_dates[league] for time in (weekday_times if date.weekday() < 5 else weekend_times)] for league in leagues}
    
    all_slots = {league: list(itertools.product(date_time_slots, court_slots)) for league, date_time_slots in league_date_time_slots.items()}
    for slots in all_slots.values():
        random.shuffle(slots)

    matches = {league: [] for league in leagues}
    team_counts = {league: {team: 0 for team in teams} for league, teams in leagues.items()}
    occupied_courts = {}

    while any(slots for slots in all_slots.values()) and any(count < matches_per_team for counts in team_counts.values() for count in counts.values()):
        for league, schedule in schedules.items():
            for i in range(len(schedule)):
                team1, team2 = schedule[i]
                if team_counts[league][team1] >= matches_per_team and team_counts[league][team2] >= matches_per_team:
                    continue
                for slot in all_slots[league]:
                    date_time, (court_location, court_numbers) = slot
                    court_key = (court_location, tuple(court_numbers))
                    if court_key not in occupied_courts or occupied_courts[court_key] <= date_time - timedelta(hours=1.5):
                        match = {}
                        match['team1'], match['team2'] = team1, team2
                        match['date_time'] = date_time
                        match['court_location'] = court_location
                        match['court_numbers'] = court_numbers
                        occupied_courts[court_key] = date_time
                        matches[league].append(match)
                        all_slots[league].remove(slot)
                        team_counts[league][team1] += 1
                        team_counts[league][team2] += 1
                        break
    
    for matches_in_league in matches.values():
        matches_in_league.sort(key=lambda x: x['date_time'])

    return matches

def main():
    st.title("Tennis Match Scheduler")

    start_date = st.date_input("Start Date", datetime(2023, 8, 1))
    end_date = st.date_input("End Date", datetime(2023, 9, 30))
    matches_per_team = st.number_input("Matches Per Team", min_value=1, value=6)
    court_type = st.selectbox("Court Type", options=[3,5])

    weekday_times = ["6:30 PM", "8:00 PM"]
    weekend_times = ["9:00 AM", "11:00 AM"]

    leagues = {
        "Men's 4.0 Singles": ["Team A", "Team B", "Team C", "Team D"],
        "Women's 4.0 Singles": ["Team E", "Team F", "Team G", "Team H"]
    }

    league_days = {
        "Men's 4.0 Singles": [1, 3], # Tuesday, Thursday
        "Women's 4.0 Singles": [5, 6] # Saturday, Sunday
    }

    court_details = {
        'Elmira': [1,2,3,4,5,6],
        'Southern boundaries': [3,4,5,6,7,8],
        'Whipoorwill': [6,7,8,9,10,11],
        'Garrett': [1,2,3,4,5,6],
        'Rock Quarry': [1,2,3,4,5,6]
    }

    matches = schedule_matches(leagues, league_days, court_details, start_date, end_date, weekday_times, weekend_times, matches_per_team, court_type)

    for league, matches_in_league in matches.items():
        st.subheader(f"{league} Matches:")
        for match in matches_in_league:
            st.text(f"{match['team1']} vs {match['team2']} at {match['court_location']} Courts {', '.join(str(x) for x in match['court_numbers'])} on {match['date_time'].strftime('%Y-%m-%d %I:%M %p')}")

if __name__ == "__main__":
    main()
