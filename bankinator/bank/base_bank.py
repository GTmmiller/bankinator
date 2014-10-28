import abc


class BankBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def authenticate(self, username, password):
        return

    @abc.abstractmethod
    def navigate(self, homepage):
        return

    @abc.abstractmethod
    def parse(self, account):
        return
