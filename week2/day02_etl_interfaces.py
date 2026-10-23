import csv
import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from day01_dataclass_models import TransactionRecord


class BaseExtractor(ABC):
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @abstractmethod
    def extract(self) -> Iterator[dict]:
        pass


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, record: dict) -> TransactionRecord:
        pass


class BaseLoader(ABC):
    @abstractmethod
    def load(self, records: Iterator[TransactionRecord]) -> int:
        pass


class CSVExtractor(BaseExtractor):
    def extract(self) -> Iterator[dict]:
        with open(file=self.filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row


class JSONExtractor(BaseExtractor):
    def extract(self) -> Iterator[dict]:
        with open(file=self.filepath, mode="r", encoding="utf-8") as f:
            for line in f:
                clean_line = line.strip()
                if clean_line:
                    yield json.loads(clean_line)


class TransactionTransformer(BaseTransformer):
    def transform(self, record: dict) -> TransactionRecord:
        return TransactionRecord.from_dict(record)


class ConsoleSummaryLoader(BaseLoader):
    def load(self, records: Iterator[TransactionRecord]) -> int:
        count = 0
        for rec in records:
            print(f"  [LOADED] {rec.transaction_id} | user: {rec.user_id} | ${rec.amount:.2f} {rec.currency}")
            count += 1
        return count


class PipelineRunner:
    def __init__(self, extractor: BaseExtractor, transformer: BaseTransformer, loader: BaseLoader) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self) -> int:
        raw_stream = self.extractor.extract()

        transformed_stream = (self.transformer.transform(record) for record in raw_stream)

        total_loaded = self.loader.load(transformed_stream)
        return total_loaded


if __name__ == "__main__":
    base_path = Path(__file__).parent.resolve()
    csv_file = base_path / "transactions.csv"
    json_file = base_path / "transactions.jsonl"

    transformer = TransactionTransformer()
    loader = ConsoleSummaryLoader()

    print("=== Running CSV Pipeline ===")
    csv_runner = PipelineRunner(
        extractor=CSVExtractor(csv_file),
        transformer=transformer,
        loader=loader,
    )
    loaded_csv = csv_runner.run()
    print(f"--- Pipeline Complete: {loaded_csv} records loaded ---\n")
    print("=== Running JSONLines Pipeline ===")
    json_runner = PipelineRunner(
        extractor=JSONExtractor(json_file),
        transformer=transformer,
        loader=loader,
    )
    loaded_json = json_runner.run()
    print(f"--- Pipeline Complete: {loaded_json} records loaded ---")
