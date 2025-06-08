import os
from pathlib import Path
import shutil
import random

from core.logger import logger
from core.config import Config


class Scrambler:
    def __init__(self, config: Config):
        self.config = config
        self.file_map = []
        self.folder_destination: str = config.dst_path
        self.extensions = config.content_path

    def scrambled_directory(self, path):
        files = [
            f
            for f in os.listdir(path)
            if f not in self.file_map
            if os.path.isfile(os.path.join(path, f))
        ]

        for file in files:
            src = os.path.join(path, file)
            ext = Path(src).suffix.lower()
            if ext not in self.extensions:
                continue

            dstFolder: str = random.choice(list(self.config.content_path.values()))
            dst = os.path.join(os.path.join(self.folder_destination, dstFolder), file)
            logger.debug(f"Scrambling file from {src} -> {dst}")
            shutil.move(src, dst)
            # self.file_map.append(file)

    def scramble_all(self):
        scrambled_any = False
        for path in self.config.paths_to_watch:
            logger.info(f"Srambling directory: {path}")
            scrambled = self.scrambled_directory(path)
            scrambled_any = scrambled_any or scrambled
        return scrambled_any
