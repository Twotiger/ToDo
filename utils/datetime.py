from datetime import datetime, timedelta

Daliy = "Daily"
WeekDays = "WeekDays"
Weekly = "Weekly"
Monthly = "Monthly"
Yearly = "Yearly"
REPEAT = [Daliy, WeekDays, Weekly, Monthly, Yearly]


def get_next_deadline(now: datetime, repeat: dict) -> datetime:
    interval_type = repeat["intervalType"]

    if interval_type == Daliy:
        return now + timedelta(days=1)
    elif interval_type == Weekly:
        return now + timedelta(days=7)
    elif interval_type == WeekDays:
        if now.weekday() == 4:
            days = 3
        elif now.weekday() == 5:
            days = 2
        else:
            days = 1
        return now + timedelta(days=days)

    elif interval_type == Monthly:
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        if now.month == 12:
            year += 1
            month = 1
        else:
            month += 1
        while 1:
            try:
                return datetime(year, month, day, hour, tzinfo=now.tzinfo)
            except ValueError:
                day = day - 1

    elif interval_type == Yearly:
        year = now.year + 1
        month = now.month
        day = now.day
        hour = now.hour
        try:
            return datetime(year, month, day, hour, tzinfo=now.tzinfo)
        except ValueError:
            return datetime(year, month, 28, hour, tzinfo=now.tzinfo)

    raise ValueError("repeat is Error")
