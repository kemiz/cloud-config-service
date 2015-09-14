class CloudConfigServiceHTTPException(Exception):

    """
    An error raised by service modules to handle errors in REST API

    """

    def __init__(self, status_code):
        self.status_code = status_code
        super(CloudConfigServiceHTTPException, self).__init__(self.__str__())

    def get_code(self):
        return self.status_code

    def to_dict(self):
        return {'error': self.__str__()}


class CloudNotFoundException(CloudConfigServiceHTTPException):

    """
    Raised when there is no cloud with requested id

    """

    def __init__(self, host_id):
        self.host_id = host_id
        super(CloudNotFoundException, self).__init__(404)

    def __str__(self):
        return 'Cannot find requested cloud: {0}'.format(self.host_id)


class ConfigurationError(Exception):

    """
    Raised when there is some error in the configuration.
    """
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)


class StorageException(Exception):

    """
    Raised when there is some error in database access.
    """
    def __init__(self, message):
        super(StorageException, self).__init__(message)
