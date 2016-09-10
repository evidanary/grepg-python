from __future__ import print_function

from abc import abstractmethod

class Command(object):
    @abstractmethod
    def execute(self): pass
