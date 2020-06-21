import levelbot.levelbot_common

from threading import Thread
from lib.utils.CancellationToken import CancellationToken
from time import sleep

from levelbot.levelbot_common import *
from lib.common import *
#
from lib.equipment import equipstaff
from lib.spells import recall
from lib.Movement import Movement
from lib.monitor.LocationMonitor import LocationMonitor
from lib.utils.ScreenshotThread import ScreenshotThread
from lib.ocr import OCR
from lib.waypoints import WAYPOINTS

class LevellingBotThread(object):
    def __init__(self, start_at_pit, meat_type):
        self.meat_type = meat_type
        self.start_at_pit = start_at_pit
        self.cancellation_token = CancellationToken()

        self.direction = [1, 1]
        self.kill_time = 30

        sc_thread = ScreenshotThread(self.cancellation_token)
        loc_monitor = LocationMonitor(sc_thread, self.cancellation_token)
        self.movement = Movement(loc_monitor, self.cancellation_token)
        self.ocr = OCR(sc_thread)

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        sleep(1)

        while not self.cancellation_token.is_cancelled:            
            if not self.start_at_pit:
                print("Equip staff")
                equipstaff()
                sleep(0.5)

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
                self.movement.followwaypoints(WAYPOINTS["blacksmith"], "blacksmith")


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

                print("Going to pit")
                self.movement.followwaypoints(WAYPOINTS["snake_pit"])

                if self.cancellation_token.is_cancelled:
                    break

                print("Equipping weapon")
                sleep(0.5)
                equipweapon()    

                if self.cancellation_token.is_cancelled:
                    break

            # ENDIF Start at pit

            self.start_at_pit = False
            print("Killing")
            kill(self.ocr, self.cancellation_token, self.kill_time)
            
            if checkifdead():
                restart()
                continue

            if self.cancellation_token.is_cancelled:
                break

            print("Running away")
            RUNAWAY_WPTS = [
                [(206, 78), 2]
            ]
            self.movement.followwaypoints(RUNAWAY_WPTS)

    def stop(self):
        self.cancellation_token.cancel()    