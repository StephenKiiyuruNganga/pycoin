"""Provides printable format for an object/instance"""


class Printable:
    def __repr__(self):
        return str(self.__dict__)
