from collections import OrderedDict

from utility.printable import Printable


class Transaction(Printable):
    def __init__(self, sender, recepient, signature, amount):
        self.sender = sender
        self.recepient = recepient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([("sender", self.sender), ("recepient", self.recepient), ("amount", self.amount)])
