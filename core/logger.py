import logging
import sys


logging.basicConfig(
    level=logging.DEBUG if "--debug" in sys.argv or "-d" in sys.argv else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
