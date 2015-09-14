class Config(object):

    def __init__(self, config):
        self._config = config
        self._validate(config)

    @staticmethod
    def _validate(config):
        if 'clouds' not in config:
            raise RuntimeError("'clouds' property is missing from the "
                               "configuration")

    @property
    def clouds(self):
        return self._config['clouds']

_instance = None


def configure(config):
    global _instance
    _instance = Config(config)


def get():
    global _instance
    return _instance
