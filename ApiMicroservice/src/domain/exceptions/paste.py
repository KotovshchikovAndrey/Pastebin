from domain.exceptions.base import DomainException


class PasteNotFoundException(DomainException):
    _message = "Paste not found"

    def __init__(self) -> None:
        super().__init__(self.message)


class InvalidPasswordException(Exception):
    _message = "Invalid password"

    def __init__(self) -> None:
        super().__init__(self.message)
