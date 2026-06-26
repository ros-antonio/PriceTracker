from datetime import datetime
from pathlib import Path


TABLE_HEADER = "| Product | Stock | Current Price | Target Price |\n| --- | --- | ---: | ---: |\n"


class Logger:
    def __init__(self, output_file_path: str, log_file_path: str = "logs/runtime.log"):
        self.output_file_path = Path(output_file_path)
        self.log_file_path = Path(log_file_path)

    def init(self) -> None:
        self.output_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.log("INFO: logger initialized")

        with self.output_file_path.open("a", encoding="utf-8") as file:
            file.write(
                f"\n\nResults from {datetime.now().strftime('%A, %d %B %Y at %H:%M')}:\n\n"
                + TABLE_HEADER
            )

    def write_result(self, result_line: str) -> None:
        with self.output_file_path.open("a", encoding="utf-8") as file:
            file.write(result_line + "\n")

    def log(self, message: str) -> None:
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file_path.open("a", encoding="utf-8") as file:
            file.write(datetime.now().strftime("%H:%M:%S - ") + message + "\n")
