import abc


class OutputBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def write(self, account, account_data):
        return
