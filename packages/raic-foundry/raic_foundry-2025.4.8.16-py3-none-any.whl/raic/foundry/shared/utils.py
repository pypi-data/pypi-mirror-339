import types
import re
from pathlib import Path
from pandas import DataFrame
from itertools import islice
from typing import Generator, Any

def chunk_iterable(iterable, chunk_size: int):
    """
    Split an iterable into chunks of a specified size. Lazy evaluation is used to avoid loading the entire iterable into memory.
    """
    if isinstance(iterable, DataFrame):
        for chunk_index in range(0, len(iterable), chunk_size):
            yield iterable[chunk_index:min(chunk_index+chunk_size, len(iterable))]
    else:
        if not isinstance(iterable, types.GeneratorType):
            iterable = iter(iterable)

        # Convert the iterable into chunks
        while chunk := list(islice(iterable, chunk_size)):
            yield chunk


def chunk_queue(queue, chunk_size: int):
    print(f'Chunking queue that currently contains {queue.qsize()} items')
    chunk = []
    while not queue.empty():
        try:
            item = queue.get(timeout=1)
            chunk.append(item)
            queue.task_done()
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        except:
            break

    if len(chunk) > 0:
        yield chunk


def is_guid(value):
    guid_regex = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
    return guid_regex.match(value)


def list_files_in_folder(source_path: str | Path | list[Path]) -> Generator[Path, Any, None]:
    if isinstance(source_path, str):
        source_path = Path(source_path)
        
    if isinstance(source_path, Path):
        for folder, dirs, files in source_path.walk(top_down=True):
            dirs.sort()  # Sort directories in-place
            files.sort()  # Sort files in-place

            # Now, 'dirs' and 'files' are in alphabetical order
            for file_string in files:
                yield Path(folder, file_string)
    else:
        iterator = sorted(source_path)

        for file_path in iterator:
            yield file_path


def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )

