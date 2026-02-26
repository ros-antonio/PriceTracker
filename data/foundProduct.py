from enums import FoundPriceType

class FoundProduct:

    def __init__(self, tag: str, link: str, priceFound=-1.0, foundPriceType=FoundPriceType.UNKNOWN, stoc="unknown"):
        self.tag = tag
        self.link = link
        self.priceFound = priceFound
        self.foundPriceType = foundPriceType
        self.stoc = stoc

    def __str__(self):
        return f'| [{self.tag}]({self.link}) | {self.stoc} | {self.__getPriceStatusSymbol()}{int(self.priceFound)} |'
    
    def __getPriceStatusSymbol(self) -> str:
        match self.foundPriceType:
            case FoundPriceType.LOWER_THAN_LAST:
                return '<code style="color: green">&#8595;</code>'
            case FoundPriceType.HIGHER_THAN_LAST:
                return '<code style="color: red">&#8593;</code>'
            case FoundPriceType.EQUAL_TO_LAST:
                return '<code style="color: gray">&#61;</code>'
            case _:
                return ''