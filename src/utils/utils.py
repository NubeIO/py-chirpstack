import datetime
import urllib.parse


class Utils:

    @classmethod
    def encode_time(cls, ts):
        return urllib.parse.quote_plus(ts.strftime('%Y-%m-%dT%H:%M:%SZ'))

    @classmethod
    def time_now(cls):
        return datetime.datetime.now()

    @classmethod
    def day_subtract(cls, days):
        now = Utils.time_now()
        sub_days = datetime.timedelta(days=days)
        return now - sub_days
