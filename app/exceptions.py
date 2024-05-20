from fastapi import HTTPException, status


class AppException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectPassword(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect password"


class UserNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such user"


class CredentialsError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"


class InvalidPayloadToken(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid token's payload"


class UserAlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "A user with these credentials already exists"


class ExpireTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has already expired"


class FakeRefreshToken(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Provided token was faked"
