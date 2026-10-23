from itertools import islice
from collections.abc import Iterator
from typing import Any
from typing import Optional
from typing import Union
def clean_amount(value: Union[float, str]) -> float:
   if isinstance(value,str):
        cleaned_value=float(value.strip().replace('$',""))
        return cleaned_value
   return float(value)


print("Cleaned 1:", clean_amount("$49.99"))
print("Cleaned 2:", clean_amount(15.5))


def get_contact_email(user: dict) -> str|None:
    if isinstance(user.get('email'),str):
        return user.get('email',None)
    return None
# Test 2: Optional email
print("Email 1:", get_contact_email({"name": "Alice", "email": "alice@data.com"}))
print("Email 2:", get_contact_email({"name": "Bob"}))
    
def stream_batches(records: list, batch_size: int) -> Iterator[list]:
        for i in range(0,len(records),batch_size):
            yield records[i:i+batch_size]

sample_data = [1, 2, 3, 4, 5]
for batch in stream_batches(sample_data, batch_size=2):
    print("Batch:", batch)