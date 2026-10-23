from dataclasses import field
from pathlib import Path
import json
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class TransactionRecord:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: str
    status: str = "pending"
    tags: tuple[str,...] = field(default_factory=tuple)
    def __post_init__(self)->None:
        if(not self.transaction_id.strip()  or not self.user_id.strip()):
           raise ValueError('Data was recieved with invalid transactionid or userid')
        if(self.amount<=0.0):
           raise ValueError('value must be more than zero')    
        if(self.currency not in ["USD", "EUR", "GBP", "CAD"]):
           raise ValueError('Invalid currrency')
    
    @classmethod
    def from_dict(cls, data: dict) -> TransactionRecord:
        raw_amt = data.get("amount", 0)
        if isinstance(raw_amt, str):
            amt = float(raw_amt.strip().replace("$", "").replace(",", ""))
        else:
            amt = float(raw_amt)
        curr = str(data.get("currency", "")).strip().upper()
        return cls(
            transaction_id=str(data.get("transaction_id", "")).strip(),
            user_id=str(data.get("user_id", "")).strip(),
            amount=amt,
            currency=curr,
            timestamp=str(data.get("timestamp", "")),
            status=str(data.get("status", "pending")),
            tags=tuple(data.get("tags") or ()),
        )


if __name__=="__main__":
    base_path=Path(__file__).parent.resolve()
    filepath=base_path/'raw_transactions.json'
    valid_records: list[TransactionRecord] = []
    quarantine_records: list[dict] = []
    with open(file=filepath,mode='r',encoding='utf-8') as f:
        data=json.load(f)
        for item in data:
          try:
            record=TransactionRecord.from_dict(item)
            valid_records.append(record)
          except(ValueError,TypeError,KeyError) as err:
            quarantine_records.append({
                'record':item,
                'error':str(err)
            })
        print(f"Valid records: {len(valid_records)}")
        print(f"Quarantined records: {len(quarantine_records)}")