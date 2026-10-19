from pathlib import Path
from itertools import islice


def stream_log_lines(filepath: Path):
    with open(file=filepath,mode='r',encoding='utf-8') as f:
        for line in f:
            clean_line=line.strip()
            if clean_line:
                yield clean_line

def parse_error_logs(lines_stream):
    for line in lines_stream:
        part=line.split(' ',3)
        if(part[2]=='ERROR'):
            yield {
                'timestamp': f"{part[0]} {part[1]}",
                'level'    : part[2],
                'message'  : part[3]
            }

def batch_stream(stream, batch_size: int = 2):
    while True:
        batch=list(islice(stream,batch_size))
        if not batch:
            break
        yield batch

if __name__== "__main__":
   basepath=Path(__file__).parent.resolve()
   input_file=basepath/'server_logs.txt'
   stream_log_lines(input_file)
   raw_stream=stream_log_lines(input_file)   
   batches=batch_stream(raw_stream,batch_size=2)
   batch_number=1
   for batch in batches:
    print(f"--- Batch {batch_number} (Size: {len(batch)}) ---")
    for item in batch:
        print(" ", item)
    batch_number+=1