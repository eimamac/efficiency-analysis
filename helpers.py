from datetime import datetime, timedelta

def get_yesterday():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')