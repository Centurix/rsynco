from rsynco import Config


class Repository:
    """
    Storage class for hosts and jobs locally
    """
    def __init__(self):
        self.config = Config()

    def reload(self):
        self.config.data.reload()
