# Class that implements the subject/observer pattern

class Subject:
    def __init__(self):
        self.observers = set()

    def addObserver(self, who):
        self.observers.add(who)

    def removeObserver(self, who):
        self.observers.discard(who)

    def dispatch(self, message):
        for observers in self.observers:
            observers.notify(message)
