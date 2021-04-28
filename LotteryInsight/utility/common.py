import os
import csv
import typing

from loguru import logger


def download_csv(data: typing.List, filepath: str, column_names: typing.List):
    row_count = len(data)
    is_file_exit = os.path.isfile(filepath)
    mode = "a" if is_file_exit else "w"
    with open(filepath, mode, newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not is_file_exit:
            writer.writerow(column_names)
        process_percentage = [int(i * 0.1 * row_count) for i in range(0, 10)]
        for idx, row in enumerate(data):
            writer.writerow(row)
            if idx in process_percentage:
                logger.debug(
                    f"{process_percentage.index(idx) * 10} % ({idx}/{row_count}) has already processed"
                )
