import csv
from collections import defaultdict
from datetime import datetime, timedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import case_reader

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
import tempfile
from helpers import get_yesterday

def parse_online_journal():
    # Use the JSON key you downloaded when you set up the Google Cloud Project
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./sheetsapi-11111203ea88502.json', scope)
    client = gspread.authorize(creds)

    # Open the Google spreadsheet by its name (make sure you have access to it)
    sheet = client.open("journalEM").sheet1

    # Get all values from the worksheet
    data = sheet.get_all_values()

    with open('journal.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def make_efficiency_log():
    with open('efficiency_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Efficiency'])
        for i in range(0, masteriux.get_days_count()):
            day_efficiency = masteriux.get_day(i).get_day_efficiency()

            date_str = masteriux.get_day(i).get_date()
            date = datetime.strptime(date_str, '%Y-%m-%d')
            timestamp = int(date.timestamp())
            date_formatted = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

            writer.writerow([date_formatted, day_efficiency])


# writes a csv file with the date and the duration of each activity
def make_duration_log():
    with open('duration_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Activity', 'Duration'])
        for i in range(0, masteriux.get_days_count()):
            date_str = masteriux.get_day(i).get_date()
            date = datetime.strptime(date_str, '%Y-%m-%d')
            timestamp = int(date.timestamp())
            date_formatted = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            for activity in masteriux.get_day(i).count_duration_per_activity():
                writer.writerow(
                    [date_formatted, activity, masteriux.get_day(i).count_duration_per_activity()[activity]])


def make_weekly_efficiency():
    # Read the input CSV file
    input_file_path = 'efficiency_log.csv'
    output_file_path = 'weekly_efficiency_log.csv'
    with open(input_file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        efficiency_log = {datetime.strptime(row[0], '%Y-%m-%d'): float(row[1]) for row in reader}

    # Calculate the weekly average efficiency
    weekly_averages = {}
    current_week_start = min(efficiency_log.keys()).date()
    current_week_start -= timedelta(days=current_week_start.weekday())
    while current_week_start <= max(efficiency_log.keys()).date():
        current_week_end = current_week_start + timedelta(days=6)
        current_week_dates = [d for d in efficiency_log.keys() if current_week_start <= d.date() <= current_week_end]
        current_week_efficiencies = [efficiency_log[d] for d in current_week_dates]
        weekly_average = round(sum(current_week_efficiencies) / len(current_week_efficiencies), 2)
        weekly_averages[current_week_start.strftime('%Y-%m-%d')] = weekly_average
        current_week_start += timedelta(days=7)

    # Write the output CSV file
    with open(output_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Week Start Date', 'Weekly Average Efficiency'])
        for week_start_date, weekly_average in weekly_averages.items():
            writer.writerow([week_start_date, weekly_average])


def activity_time_distribution():
    activity_time_dict = defaultdict(list)
    with open('journal.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            activity = row[2]  # Activity is in the third column
            hour = int(row[1])  # Hour is in the second column
            activity_time_dict[activity].append(hour)

    # Write the average start times to a CSV file
    with open('activity_time_distribution.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Activity', 'Average Start Time'])
        for activity, hours in activity_time_dict.items():
            average_start_time = sum(hours) / len(hours)
            writer.writerow([activity, average_start_time])


def make_activity_charts(file_name, end_date_str):
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    start_date = end_date - timedelta(days=7)

    # Read data from .csv file
    data = pd.read_csv(file_name)
    data['Date'] = pd.to_datetime(data['Date'])
    # Filter data to include only the last 7 days
    last_7_days_data = data[(data['Date'] > start_date) & (data['Date'] <= end_date)]
    # Group by activity and sum the durations for the last 7 days
    grouped_data_7_days = last_7_days_data.groupby('Activity')['Duration'].sum()
    # Filter data to include only the end date
    end_date_data = data[data['Date'] == end_date]
    # Group by activity and sum the durations for the end date
    grouped_data_end_date = end_date_data.groupby('Activity')['Duration'].sum()
    # Create a PDF
    c = canvas.Canvas('activity_charts.pdf', pagesize=letter)
    width, height = letter
    # Define a list of colors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf', '#1a55FF', '#55a3FF', '#6F00D2', '#8F00B3',
              '#D2005F', '#FF0000']
    # Create a color dictionary that maps activities to colors
    color_dict = dict(zip(data['Activity'].unique(), colors))
    # Create the pie chart for the last 7 days
    fig, ax = plt.subplots()
    ax.pie(grouped_data_7_days, labels=grouped_data_7_days.index, autopct='%1.1f%%',
           colors=[color_dict.get(activity, 'w') for activity in grouped_data_7_days.index])
    ax.axis('equal')
    plt.title('Last Week')
    # Save the pie chart to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        plt.savefig(temp.name)
        temp.seek(0)

        # Insert the chart into the PDF
        c.drawImage(temp.name, 0, height / 2, width, height / 2)
    plt.close(fig)
    # Create the pie chart for the end date
    fig, ax = plt.subplots()
    ax.pie(grouped_data_end_date, labels=grouped_data_end_date.index, autopct='%1.1f%%',
           colors=[color_dict.get(activity, 'w') for activity in grouped_data_end_date.index])
    ax.axis('equal')
    plt.title(end_date_str)
    # Save the pie chart to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        plt.savefig(temp.name)
        temp.seek(0)
        # Insert the chart into the PDF
        c.drawImage(temp.name, 0, 0, width, height / 2)
    plt.close(fig)
    # Save the PDF
    c.showPage()
    c.save()



parse_online_journal()
masteriux = case_reader.readcsv()

print(f'total days: {masteriux.get_days_count()}')
print()
print(masteriux.print_first_and_last_days())
print()

# './journal.csv' 
make_duration_log()
make_efficiency_log()
make_weekly_efficiency()
activity_time_distribution()

make_activity_charts('duration_log.csv', get_yesterday())

# todo
# efficiency liner graph weeks, last 30 days, last 120 days
# send_report()
# then configure to send every day/ week
