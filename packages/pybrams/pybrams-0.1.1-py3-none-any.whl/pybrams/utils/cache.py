import os
import shutil
import glob
from typing import Any, List, Optional, Union, Dict, Literal
import logging
from pybrams.utils.config import Config

logger = logging.getLogger(__name__)


class Cache:
    root = os.path.join(".", ".pybrams_cache")
    data = {}

    @classmethod
    def clear(cls) -> None:
        logger.info("Clearing cache")
        shutil.rmtree(cls.root, ignore_errors=True)
        cls.data = {}

    @classmethod
    def cache(cls, key: str, data: Any, json: bool = True) -> None:

        if Config.get(__name__, "use"):
            if not os.path.exists(cls.root):
                os.mkdir(cls.root)

            path = f"{key}.json" if json else key
            mode = "w" if json else "wb"

            with open(os.path.join(cls.root, path), mode) as file:
                file.write(data)

            if json:
                cls.data[key] = data

            logger.info(f"Storing {key}")

    @classmethod
    def get(cls, key: str, json: bool = True) -> Union[Any, Literal[False]]:
        if Config.get(__name__, "use"):
            path = f"{key}.json" if json else key
            mode = "r" if json else "rb"

            if json and key in cls.data:
                return cls.data[key]

            if not os.path.exists(os.path.join(cls.root, path)):
                return False

            with open(os.path.join(cls.root, path), mode) as file:
                data = file.read()
                cls.data[key] = data
                logger.info(f"Retrieving {key}")
                return data

        return False

    @classmethod
    def remove(cls, key: str, json: bool = True) -> bool:
        path = f"{key}.json" if json else key
        full_path = os.path.join(cls.root, path)

        if json and key in cls.data:
            del cls.data[key]

        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info(f"Removed {key}")
            return True

        return False

    @classmethod
    def stats(cls) -> Dict[str, Union[int, float]]:
        if not os.path.exists(cls.root):
            return {
                "number_of_files": 0,
                "total_size_bytes": 0,
                "total_size_kb": 0,
                "total_size_mb": 0,
            }

        total_size = 0
        file_count = 0

        for root, _, files in os.walk(cls.root):
            for file in files:
                file_count += 1
                total_size += os.path.getsize(os.path.join(root, file))

        return {
            "number_of_files": file_count,
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }
