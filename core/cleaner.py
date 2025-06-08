import os
import shutil
import logging
from pathlib import Path
from watchdog.events import FileSystemEventHandler

from core.logger import logger
from core.config import Config


class Cleaner(FileSystemEventHandler):

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.extensions = self.config.content_path
        self.folder_destination: str = config.dst_path

    def __organize_file(self, filepath: str) -> None:
        try:
            i = 0
            new_name = os.path.basename(filepath)
            ext = Path(filepath).suffix.lower()
            extDir: str = self.extensions.get(ext, "")
            if os.path.dirname(filepath).split(os.path.sep)[-1] == extDir:
                logging.debug(f"Skipping {filepath}")
                return
            split_name = os.path.splitext(new_name)
            while os.path.exists(os.path.join(self.folder_destination, new_name)):
                logger.debug(f"Renaming {new_name}")
                new_name = split_name[0] + "(" + str(i) + ")" + split_name[1]
                i += 1
            if ext in self.extensions:
                dst = os.path.join(
                    os.path.join(self.folder_destination, extDir), new_name
                )
                logger.debug(f"Moving file from {filepath} to {dst}")
                shutil.move(filepath, dst)
        except FileNotFoundError:
            logger.error(f"Error moving file {filepath}")
            pass
        except Exception as e:
            logger.error("An error occured: " + str(e))

    def on_created(self, event):
        if event.is_directory:
            return
        logger.debug(f"File created: {event.src_path}")
        self.__organize_file(str(event.src_path))

    def on_modified(self, event) -> None:
        if event.is_directory:
            return
        logger.debug(f"File modified: {event.src_path}")
        self.__organize_file(str(event.src_path))

    def organize_directory(self, directory) -> None:
        logger.info(f"Organizing directory: {directory}")
        try:
            for filename in os.listdir(directory):
                if not os.path.isdir(
                    os.path.join(directory, filename),
                ):
                    filepath = os.path.join(directory, filename)
                    self.__organize_file(filepath)
                else:
                    logger.debug("Directory found " + filename)
        except Exception as e:
            logger.error(f"Failed to organize directory '{directory}': {e}")

        # return super().on_modified(event)
