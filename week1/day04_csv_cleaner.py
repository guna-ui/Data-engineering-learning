from pathlib import Path
import csv


Base_dir=Path(__file__).resolve().parent


def read_raw_csv(filepath: str) -> list:
    with open(filepath,mode='r',encoding='utf-8',newline="") as f:
        data=[]
        reader=csv.DictReader(f)
        for row in reader:
            data.append(row)
        return data

def clean_records(records:dict)->list:
    cleaned_rows=[]
    for record in records:
        customer=record['customer'].strip()
        status=record['status'].strip().lower()
        amount_str=record['amount'].strip()
        if not customer or not amount_str:
            continue
        try:
                amount=float(amount_str)
                order_id=int(record['order_id'])
                cleaned_rows.append({
                    'order_id':order_id,
                    'customer':customer,
                    'amount':amount,
                    'status':status
                })
        except ValueError:
                print(f"Error while clearning records")    
    return cleaned_rows
def write_clean_csv(filepath: Path, data: list) -> None:
    if(data is None):
            return
    fieldnames=list(data[0].keys())
    with open(filepath,mode='w',encoding='utf-8',newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

        

if __name__=="__main__":
    csv_file=Base_dir/'dirty_sales.csv'
    raw_data=read_raw_csv(csv_file)
    cleaned_data=clean_records(raw_data)

    target_file = Base_dir / 'target.csv'
    write_clean_csv(target_file,cleaned_data)
    print(f"Successfully written to {target_file}")
