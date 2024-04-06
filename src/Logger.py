from .MultiLangLogger.python import Logger as _Logger

class Logger(_Logger):
    def __init__(self, name: str):
        super().__init__(name)

logger = Logger('CPA2SC')