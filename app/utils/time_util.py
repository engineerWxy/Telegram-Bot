from datetime import datetime


class TimeUtil(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    LONG_TIME_FORMAT = '%Y%m%d%H%M%S'

    @staticmethod
    def generate_time_nonce(fmt=None):
        """
        generate nonce by time
        :param fmt:
        :return:
        """
        if fmt is None:
            fmt = TimeUtil.LONG_TIME_FORMAT
        now = datetime.now()
        return now.strftime(fmt)

    @staticmethod
    def generate_timestamp(iso=False):
        """
        generate timestamp
        :param iso: iso format
        :return:
        """
        if iso is True:
            return datetime.utcnow().isoformat() + 'Z'
        return int(datetime.now().timestamp())
