import traceback
from abc import ABC, abstractmethod

from time import sleep
from logging import Logger


class CanaryScript(ABC):
    logger: Logger

    def __init__(
        self,
        logger: Logger,
        delay: int,
        count: int
    ):
        self.logger = logger
        self.delay = delay
        self.count = count
        if count < 0:
            while True:
                self.__do_invoke()
                sleep(delay)
        while count > 0:
            self.__do_invoke()
            if count <= 1:
                break
            sleep(delay)
            count -= 1

    @abstractmethod
    def invoke(self):
        pass

    def __do_invoke(self):
        try:
            self.invoke()
        except Exception as e:
            self.logger.error(
                f"Unhandled exception raised ({repr(e)})\r\n"
                f"{traceback.format_exc()}"
            )
