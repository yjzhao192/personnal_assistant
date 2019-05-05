import logging


class TestFilter(logging.Filter):

    def filter(self, record):
        if '[FILTER FLAG]' in record.msg:
            return False
        return  True
