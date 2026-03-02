from enum import Enum

class FoundPriceType(Enum):
    LOWER_THAN_LAST = 1
    HIGHER_THAN_LAST = 2
    EQUAL_TO_LAST = 3
    FIRST_PRICE_FOUND = 4
    UNKNOWN = 5