from collections import defaultdict

raw_data = [10, 20, 20, 30, 40, 10, 50, 30]
raw_events = [
    {"user_id": 1, "timestamp": 100, "action": "login"},
    {"user_id": 2, "timestamp": 105, "action": "click"},
    {"user_id": 1, "timestamp": 100, "action": "login"},    # Duplicate!
    {"user_id": 3, "timestamp": 110, "action": "purchase"},
    {"user_id": 2, "timestamp": 105, "action": "click"},    # Duplicate!
    {"user_id": 1, "timestamp": 120, "action": "logout"},   # NOT duplicate (different timestamp)
]



def remove_duplicates_simple(numbers: list) -> list:
    seen=set()
    unique_items=[]
    for n in numbers:
        if n not in seen:
            seen.add(n)
            unique_items.append(n)
    return seen,unique_items


print(remove_duplicates_simple(raw_data))


def deduplicate_events(events: list) -> list:
    seen=set()
    unique_events=[]
    for events in raw_events:
        key=(events['user_id'],events['timestamp'])
        if key not in seen:
            seen.add(key)
            unique_events.append(events)
    return unique_events

print(deduplicate_events(raw_events))


def group_events_by_user(events: list) -> dict:
    grouped=defaultdict(list)
    seen=set()
    for event in events:
        key=(event['user_id'],event['action'])
        if key not in seen:
            seen.add(key)
            grouped[event['user_id']].append(event['action'])
    return dict(grouped)


print(group_events_by_user(raw_events))


