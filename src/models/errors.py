class ModelBaseError(Exception):
    """Model Base Error"""
    MESSAGE = 'Model base error'

    def __init__(self, *args, message=''):
        super().__init__(*args)
        self.message = message or self.MESSAGE

    def __str__(self):
        return self.MESSAGE


class DoesNotExistsError(ModelBaseError):
    """Does Not Exists Error"""
    MESSAGE = 'Object does not exists'
