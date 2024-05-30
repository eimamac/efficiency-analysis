import keywords


class Day:
    long_duration = 60
    short_duration = 30
    good_stuff = keywords.good_stuff
    neutral_stuff = keywords.neautral_stuff
    bad_stuff = keywords.bad_stuff
    all_stuff = [good_stuff, neutral_stuff, bad_stuff]

    def __init__(self, arr):
        self.records = arr
        self.date = self.records[0][0]

    def get_date(self):
        return self.date

    def get_all_records(self):
        return self.records

    def get_record(self, nr):
        return self.records[nr]

    def get_all_activities(self):
        activities = []
        for i in self.records:
            if i[2] != '':
                activities.append(i[2])
        return activities

    def print_day(self):
        print()
        print('Day ---------')
        for i in self.records:
            print(i)

    def count_duration_per_activity(self):
        records = self.get_all_records()
        duration_dict = {}
        i = 0
        while i < len(records):
            hour = records[i][1]
            activities = []
            while i < len(records) and records[i][1] == hour:
                activity = records[i][2]
                if activity != '':
                    activities.append(activity)
                i += 1
            duration_per_activity = self.short_duration if len(activities) > 1 else self.long_duration
            for activity in activities:
                if activity in duration_dict:
                    duration_dict[activity] += duration_per_activity
                else:
                    duration_dict[activity] = duration_per_activity
        return dict(sorted(duration_dict.items(), key=lambda item: item[1], reverse=True))

    def get_day_efficiency(self):
        activities = self.get_all_activities()
        green_count = 0
        yellow_count = 0
        red_count = 0

        if len(activities) < 5:
            return 0
        for i in keywords.good_stuff:
            if i in activities:
                add = activities.count(i)
                green_count += add
        for i in keywords.neautral_stuff:
            if i in activities:
                add = activities.count(i)
                yellow_count += add
        for i in keywords.bad_stuff:
            if i in activities:
                add = activities.count(i)
                red_count += add

        day_efficiency = (green_count + (yellow_count * 0.8) - (red_count * 0.001)) / \
                         (green_count + yellow_count + red_count * 0.65) * 100

        return round(day_efficiency, 1)
