import logging


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[37m',     # White
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        formatter = logging.Formatter(
            "%(asctime)s %(name)s - [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        output = formatter.format(record)
        color = self.COLORS.get(record.levelname, self.RESET)
        return f"{color}{output}{self.RESET}"


logger = logging.getLogger("Game Client")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
logger.addHandler(handler)
