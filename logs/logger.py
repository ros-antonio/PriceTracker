from datetime import datetime

TABLE_BASE = "| Eticheta | Stoc Disponibil | Pret &nbsp; &nbsp; |\n| --- | --- | ---: |\n"

# Thursday, 26 February 2026 at 13:18 e la cap de sesiune de logare
class Logger:

    def __init__(self, path: str, logPath: str):
        self.outputFilePath = path
        self.logFilePath = logPath

    def init(self):
        with open(self.outputFilePath, "a", encoding="utf-8") as f:
            f.write(f'\n\nResults from {datetime.now().strftime("%A, %d %B %Y at %H:%M")}:\n\n' + TABLE_BASE)

    def writeResult(self, resultLine: str) -> None:
        with open(self.outputFilePath, "a", encoding="utf-8") as f:
            f.write(resultLine + '\n')

    def log(self, log: str):
        with open(self.logFilePath, "a", encoding="utf-8") as f:
            f.write(datetime.now().strftime("%H:%M:%S - ") + log + '\n')