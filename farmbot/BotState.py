import inspect
import logging

class BotState(object):
    def __init__(self):
        self.logger = logging.getLogger("hbbot.botstate")
        self.__hoe_index = 0

    def gethoeindex(self):
        return self.__hoe_index

    def sethoeindex(self, index):
        self.__hoe_index = index

    def incrementhoeindex(self):
        self.__hoe_index += 1

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        self.logger.debug("incrementhoeindex " + calframe[1][3] + " " + str(self.__hoe_index))

        if self.__hoe_index == 4:
            print("overflow")            