class PublisherThread(object):
    def __init__(self):
        self.subscribers = []

    def __hassubscriber(self, callback):
        for subscriber in self.subscribers:
            if subscriber == callback:
                return True
        
        return False

    def subscribe(self, callback, args=None):
        item = (callback, args)
        if not self.__hassubscriber(item):
            self.subscribers.append(item)
            return True

        return False

    def unsubscribe(self, callback):
        try:
            for subscriber in self.subscribers:
                cb = subscriber[0]

                if cb == callback:
                    self.subscribers.remove(subscriber)
                    return True

            return False                
        except ValueError:
            return False

    def notify(self, payload=None):
        for subscriber in self.subscribers:
            callback = subscriber[0]
            callback(payload, subscriber[1])