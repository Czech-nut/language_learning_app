from fastapi import status


class BadRequest(Exception):
    def __init__(self, detail: str = "User passed unprocessable data"):
        self.title = "Bad Request"
        self.detail = detail
        self.status = status.HTTP_400_BAD_REQUEST


class NotFound(Exception):
    def __init__(self, detail: str = "Such object does not exist"):
        self.title = "Not Found"
        self.detail = detail
        self.status = status.HTTP_404_NOT_FOUND


class DuplicateData(Exception):
    def __init__(self, detail: str = "Such object already exists"):
        self.title = "Duplicate data"
        self.detail = detail
        self.status = status.HTTP_409_CONFLICT


class Unauthorised(Exception):
    def __init__(self, detail: str = "User is unauthorised"):
        self.title = "Unauthorised"
        self.detail = detail
        self.status = status.HTTP_401_UNAUTHORIZED


class Forbidden(Exception):
    def __init__(self, detail: str = "Not enough permissions to perform this action"):
        self.title = "Forbidden"
        self.detail = detail
        self.status = status.HTTP_403_FORBIDDEN
