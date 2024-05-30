from day import Day


class DayCase:
    def __init__(self):
        self.days = []

    def add_day(self, day: Day):
        self.days.append(day)

    def get_day(self, nr) -> Day:
        return self.days[nr]

    def get_all_days(self):
        return self.days

    def get_days_count(self):
        return len(self.days)

    def print_all_days_dates(self):
        for i in self.days:
            print(i.get_date())

    def print_object_list(self):
        for day in self.days:
            print()
            print('Day ---------')
            for i in day.records:
                print(i)

    def print_first_and_last_days(self):
        if self.days:  # Check if the list is not empty
            return f"Day range: {self.days[0].get_date()} - {self.days[-1].get_date()}"
        else:
            return "No days in the list."
