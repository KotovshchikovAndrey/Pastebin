from enum import IntEnum


class ExpirationEnum(IntEnum):
    NEVER = -1
    DROP_AFTER_READ = 0
    TEN_MINUTES = 60 * 10
    ONE_HOUR = 60 * 60
    ONE_DAY = 60 * 60 * 24
    ONE_WEEK = 60 * 60 * 24 * 7
    TWO_WEEK = 60 * 60 * 24 * 14
    ONE_MONTH = 60 * 60 * 24 * 31
    ONE_YEAR = 60 * 60 * 24 * 365
