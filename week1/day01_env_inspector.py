from pathlib import Path
from typing import List,Dict,Any

def format_bytes(size_bytes)->str:
    if size_bytes < 1024:
        return f"{size_bytes} B"

    units = ["KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)

    for unit in units:
        size /= 1024.0

        if size < 1024.0:
            return f"{size:.2f} {unit}"

    return f"{size:.2f} EB"


def inspect_directory(target_path: Path, top_n: int = 5) -> Dict[str, Any]:
    path=Path(target_path)
    total_files = 0
    total_bytes = 0
    extension_stats = {}
    
    file_records = [] 
    actual_path=path.resolve()
    if not actual_path.exists():
       raise FileNotFoundError(f"Target path does not exist: {actual_path}")
    if not actual_path.is_dir():
        raise NotADirectoryError(f"Target path is not a directory: {actual_path}")

    for entry in actual_path.rglob("*"):
        try:
            if not entry.is_file():
                continue
            size = entry.stat().st_size
            extension = entry.suffix.lower() if entry.suffix else "(no_extension)"

            total_files += 1
            total_bytes += size

            if extension not in extension_stats:
                extension_stats[extension] = {
                    "count": 0,
                    "total_bytes": 0
                }
            extension_stats[extension]["count"] += 1
            extension_stats[extension]["total_bytes"] += size

            file_records.append({
                "path": str(entry.relative_to(actual_path)),
                "size_bytes": size,
                "extension": extension
            })
        except (PermissionError, OSError):
            continue

    for ext, data in extension_stats.items():
        data["formatted_size"] = format_bytes(data["total_bytes"])

    largest_files = sorted(file_records, key=lambda x: x["size_bytes"], reverse=True)[:top_n]
    for item in largest_files:
        item["formatted_size"] = format_bytes(item["size_bytes"])

    return {
        "root_directory": str(actual_path),
        "total_files": total_files,
        "total_bytes": total_bytes,
        "formatted_total_size": format_bytes(total_bytes),
        "extension_breakdown": extension_stats,
        "largest_files": largest_files
    }


if __name__ == "__main__":
    import json
    import sys

    scan_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    print(f"Scanning directory: {scan_dir.resolve()} ...\n")
    report = inspect_directory(scan_dir, top_n=5)
    print(json.dumps(report, indent=2))