from datetime import tzinfo, timedelta


class Eastern_Standard_Timezone(tzinfo):
    """
    Defines the EST for use with time objects
    """

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "-05:00"

    def __repr__(self):
        return f"{self.__class__.__name__}()"
