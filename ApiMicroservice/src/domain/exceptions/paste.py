from domain.exceptions.base import DomainException


class PasteNotFoundException(DomainException):
    _message = "Paste not found"

    def __init__(self) -> None:
        super().__init__(self._message)


class CategoryNotFoundException(DomainException):
    _message = "Category not found"

    def __init__(self) -> None:
        super().__init__(self._message)


class InvalidPasswordException(DomainException):
    _message = "Invalid password"

    def __init__(self) -> None:
        super().__init__(self._message)
