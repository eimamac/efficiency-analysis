def make_sendable_week_report(file_name, end_date_str):
    import pandas as pd
    import matplotlib.pyplot as plt
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from datetime import datetime, timedelta
    import tempfile

    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    start_date = end_date - timedelta(days=7)

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

    # Create the pie chart for the last 7 days
    fig, ax = plt.subplots()
    ax.pie(grouped_data_7_days, labels=grouped_data_7_days.index, autopct='%1.1f%%')
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
    ax.pie(grouped_data_end_date, labels=grouped_data_end_date.index, autopct='%1.1f%%')
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