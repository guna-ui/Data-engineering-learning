from collections import defaultdict
raw_transactions = [
    {"user_id": " u1 ", "amount": "150", "status": "completed"},
    {"user_id": "U2", "amount": "20", "status": "refunded"},
    {"user_id": "u1", "amount": "300", "status": "completed"},
    {"user_id": " u3 ", "amount": "500", "status": "COMPLETED"},
    {"user_id": "U4", "amount": "100", "status": "completed"},
]

# List of flagged bot accounts to filter out
bot_ids = ["u2", "u4"]

transform=[{'user_id':raw['user_id'].strip().lower(),'amount':int(raw['amount']),'status':raw['status'].lower()} for raw in raw_transactions]

cleaned=[trans 
     for trans in transform 
     if trans['user_id'] not in bot_ids and trans['status']=='completed']


def data_transform(data:list)->dict:
    grouped=defaultdict(int)
    for trans in data:
            grouped[trans['user_id']]+=trans['amount']
    return dict(grouped)

x=data_transform(cleaned)

print(x)


def log_query(query_name, *args, **kwargs):
    print(f"Executing: {query_name}")
    print(f"Positional params: {args}")
    print(f"Keyword params: {kwargs}")


# Calling it with different database parameters:
log_query("fetch_users", "active", "US", limit=100, timeout=30)


def connect_database(host, port, database_name):
    print(f"Connecting to {database_name} at {host}:{port}...")

db_config = {"host": "10.0.0.1", "port": 5432, "database_name": "analytics_db"}

connect_database(**db_config)


nested_order = {
    "order_id": 901,
    "customer": {
        "name": "Sarah Connor",
        "city": "Los Angeles"
    },
    "payment": {
        "amount": 250.75,
        "status": "completed"
    },
    "internal_notes": "flagged for review",
    "debug_id": "xyz-9988-trace"
}


def flatten_order(order: dict) -> dict:
    return {
        "order_id":order['order_id'],
        "customer_name":order['customer']['name'],
        "customer_citry":order['customer']['city'],
        "amount":order['payment']['amount'],
        'status':order['payment']['status'],
        'internal_notes':order['internal_notes'],
        'debug_id':order['debug_id']
    }

flat=flatten_order(nested_order)


def drop_fields(record: dict, *fields_to_drop) -> dict:
    # print(record.items())
    return {key:value for key,value in record.items() if key not in fields_to_drop}

print(drop_fields(flat,"internal_notes", "debug_id"))