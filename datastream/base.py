class BaseSubtitleStreamServer(object):
    def __init__(self):
        pass

    def add_subscriber(self, callback):
        raise NotImplementedError
