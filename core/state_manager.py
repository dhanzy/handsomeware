import json
import os
from pathlib import Path
import random
import string
from typing import Any

from core.logger import logger


STATE_FILE = Path("data/state.json")
DEFAULT_DURATION_SECONDS = 60 * 10


DEFAULT_STATE = {
    "scrambled": False,
    "passcode_entered": False,
    "passcode": None,
    "start_time": None,
}


class StateManager:
    def __init__(
        self,
    ):
        self._state = self.__load_or_create_state()

    def __load_or_create_state(self):
        os.makedirs(STATE_FILE.parent, exist_ok=True)

        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as f:
                logger.info("Loading saved state.")
                return json.load(f)

        logger.info("Creating new state")
        passcode = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        state = {
            "start_time": None,
            "scrambled": False,
            "passcode": passcode,
            "passcode_entered": False,
        }
        self.__save_state(state)
        return state

    def get(self, key) -> Any:
        return self._state.get(key)

    def set(self, key, value):
        self._state[key] = value
        self.__save_state()

    def __save_state(self, state=None):
        if state is not None:
            self._state = state

        with open(STATE_FILE, "w") as f:
            json.dump(self._state, f, indent=2)

    def get_remaining_time(self):
        return self._state["remaining_time"]

    def get_passcode(self):
        return self._state["passcode"]

    def is_scrambled(self):
        return self._state.get("scrambled", False)

    def is_passcode_entered(self):
        return self._state.get("passcode_entered", False)

    def reset(self):
        passcode = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self._state["passcode"] = passcode
        self._state["scrambled"] = False
        self._state["passcode_entered"] = False
        self._state["start_time"] = None
        self.__save_state()
