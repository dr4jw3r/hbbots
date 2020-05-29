import levelbot.levelbot_common

from threading import Thread
from lib.CancellationToken import CancellationToken
from time import sleep

from levelbot.levelbot_common import *
from lib.common import *

class LevellingBotThread(object):
    def __init__(self, start_at_pit, meat_type):
        self.meat_type = meat_type
        self.start_at_pit = start_at_pit
        self.cancellation_token = CancellationToken()

        self.direction = [1, 1]
        self.kill_time = 60

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        sleep(1)

        while not self.cancellation_token.is_cancelled:            
            if not self.start_at_pit:
                print("Equip staff")
                equipstaff()

                if self.cancellation_token.is_cancelled:
                    break

                print("First recall")
                recall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Chugging pots")
                chugpots()

                if self.cancellation_token.is_cancelled:
                    break

                has_eaten_meat = False
                for i in range(2):
                    if self.cancellation_token.is_cancelled:
                        break

                    print("Eating Meat")
                    if self.meat_type is not None:
                        has_meat = eatmeat(self.meat_type)

                        if has_meat:
                            has_eaten_meat = True

                        sleep(0.5)
            
                    if self.cancellation_token.is_cancelled:
                        break

                    print("Disenchanting")
                    disenchant(self.cancellation_token)
                    sleep(0.5)

                if self.cancellation_token.is_cancelled:
                    break

                print("Going to blacksmith")
                gotoblacksmith_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break
                
                print("Repairing gear")
                repairgear(self.cancellation_token)
                
                if self.cancellation_token.is_cancelled:
                    break

                print("Selling items")
                sellitems(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Second recall")
                recall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break            

                if not has_eaten_meat:
                    print("Eating")
                    eat(self.cancellation_token, 3)

                if self.cancellation_token.is_cancelled:
                    break

                print("Equipping weapon")
                sleep(0.5)
                equipweapon()                        

                if self.cancellation_token.is_cancelled:
                    break

                print("Going to pit")
                PIT_WPTS = [
                    [160, 85],
                    [211, 64],
                    [215, 59]
                ]
                followwpts(self.cancellation_token, PIT_WPTS)

                if self.cancellation_token.is_cancelled:
                    break

            # ENDIF Start at pit

            self.start_at_pit = False
            print("Killing")
            kill(self.cancellation_token, self.kill_time)
            
            if checkifdead():
                restart()
                continue

            if self.cancellation_token.is_cancelled:
                break

            print("Running away")
            RUNAWAY_WPTS = [
                [206, 78]
            ]
            followwpts(self.cancellation_token, RUNAWAY_WPTS)

    def stop(self):
        self.cancellation_token.cancel()    