import json
from json import JSONDecodeError
from pathlib import Path
from typing import Callable, Dict, List

from pharcobial.logging import game_logger


def safe_load(path: Path) -> Dict:
    """
    Will delete file if the JSON is corrupt and return an empty dict.
    """
    if not path.is_file():
        return {}

    text = path.read_text()
    data = {}
    try:
        data = json.loads(text)
    except JSONDecodeError:
        game_logger.error("JSON file '{path}' corrupted. Deleting.")
        path.unlink()

    return data


def safe_dump(path: Path, data: Dict):
    path.unlink(missing_ok=True)
    path.write_text(json.dumps(data))


def safe_load_csv(path: Path, cb: Callable = str) -> List[List]:
    if not path.is_file():
        return []

    rows: List[List] = []
    with open(path, "r") as file:
        lines = file.readlines()

    for line in lines:
        row: List = [cb(x.strip()) for x in line.split(",")]
        rows.append(row)

    return rows
