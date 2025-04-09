class EmptyJoinPathSegments(Exception):

    def __init__(self,
                 message='There are not segments to concatenate'):
        self.message = message
        super().__init__(self.message)


class BucketNotExist(Exception):

    def __init__(self,
                 message='The bucket doesn\'t exist'):
        self.message = message
        super().__init__(self.message)
