from rsynco import Config


class Repository:
    """
    Storage class for hosts and jobs locally
    """
    def __init__(self):
        self.config = Config()

    def reload(self):
        self.config.data.reload()

    def check_section(self, section_name):
        if section_name not in self.config.data.keys():
            self.config.add_section(section_name)
