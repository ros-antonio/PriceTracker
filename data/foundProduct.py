from enums import FoundPriceType

OUT_OF_STOCK_LIST = ["Stoc epuizat", "Nu este in stoc", "stoc epuizat", "nu este in stoc",
                      "Stoc indisponibil", "stoc indisponibil", "out of stock", "Out of stock"]
LIMITED_STOCK_LIST = ["Ultimul", "Ultimele", "expus", "ultimul", "ultimele", "expus", "Limitat", "limitat"]

class FoundProduct:

    def __init__(self, tag: str, link: str, priceFound=-1.0, foundPriceType=FoundPriceType.UNKNOWN, stoc="unknown"):
        self.tag = tag
        self.link = link
        self.priceFound = priceFound
        self.foundPriceType = foundPriceType
        self.stoc = stoc

    def __str__(self):
        return f'| [{self.tag}]({self.link}) | {self.__getStocStatus()} | {self.__getPriceStatusSymbol()}{int(self.priceFound)} |'
    
    def __getPriceStatusSymbol(self) -> str:
        match self.foundPriceType:
            case FoundPriceType.LOWER_THAN_LAST:
                return '<code style="color: lime">&#8595;</code>'
            case FoundPriceType.HIGHER_THAN_LAST:
                return '<code style="color: red">&#8593;</code>'
            case FoundPriceType.EQUAL_TO_LAST:
                return '<code style="color: gray">&#61;</code>'
            case _:
                return ''
            
    def __getStocStatus(self) -> str:
        if self.stoc in OUT_OF_STOCK_LIST:
            return f'<code style="color: red">{self.stoc}</code>'
        if any(cuvant in self.stoc for cuvant in LIMITED_STOCK_LIST):
            return f'<code style="color: darkorange">{self.stoc}</code>'
        if self.stoc != "unknown":
            return f'<code style="color: green">{self.stoc}</code>'
        return self.stoc
        