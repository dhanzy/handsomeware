#!/usr/bin/env python3

import argparse
from datetime import datetime
from watchdog.observers import Observer
from core.logger import logger
from core.config import Config
from core.scrambler import Scrambler
from core.state_manager import StateManager
from core.ui import UI
from core.cleaner import Cleaner
import time
import threading
import sys

from core.util import get_remaining_seconds


def create_parser():
    parser = argparse.ArgumentParser(description="Handsomeware file arranger")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset program.")
    return parser.parse_args()


def start_observer(cleaner: Cleaner, config: Config, state: StateManager):
    observer = Observer()

    for path in config.paths_to_watch:
        logger.debug(f"Watching path: {path}")
        observer.schedule(cleaner, path, recursive=True)
    observer.start()
    logger.info("Observer started.")
    try:
        observer_running = True
        while True:
            start_time = state.get("start_time")
            passcode_entered = state.get("passcode_entered")
            secs = get_remaining_seconds(start_time, config.time_limit)

            if not start_time:
                time.sleep(1)
                continue

            if secs <= 0 and not passcode_entered and observer_running:
                observer.stop()
                observer.join()
                observer_running = False
                logger.info("Time expired and passcode not entered. Observer stopped.")

            elif passcode_entered and not observer_running:
                logger.info("Passcode entered. Restarting observer.")
                observer = Observer()
                for path in config.paths_to_watch:
                    logger.debug(f"Watching path: {path}")
                    observer.schedule(cleaner, path, recursive=True)
                    cleaner.organize_directory(path)
                observer.start()
                observer_running = True
                logger.info("Observer restarted.")
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    args = create_parser()
    config = Config()
    state = StateManager()
    if args.reset:
        state.reset()
        logger.info("Application reset successfull")
        sys.exit(0)
    if not state.get("start_time"):
        now = datetime.now().isoformat()
        state.set("start_time", now)
    cleaner = Cleaner(config)

    passcode_entered = state.get("passcode_entered")
    secs = get_remaining_seconds(state.get("start_time"), config.time_limit)
    if passcode_entered or secs > 0:
        for path in config.paths_to_watch:
            cleaner.organize_directory(path)

    observer_thread = threading.Thread(
        target=start_observer, args=(cleaner, config, state), daemon=True
    )
    observer_thread.start()
    scramber = Scrambler(config)
    ui = UI(config, state, scramber)
    ui.run()


if __name__ == "__main__":
    main()
