###########
from threading import Thread
from time import sleep, time
from math import ceil
###########
from lib.CancellationToken import CancellationToken
###########
from farmbot.common import *
from lib.common import *
from levelbot.levelbot_common import equipweapon
from farmbot.harvester import Harvester
from farmbot.planter import Planter
###########
from lib.threads.killaround import KillAroundThread

class FarmThread(object):
    def __init__(self, crop_type, start_at_farm):
        self.start_at_farm = start_at_farm
        self.crop_type = crop_type
        self.num_hoes = 4
        self.num_seed_bags_per_hoe = 9
        self.cancellation_token = CancellationToken()

        self.harvester = Harvester()
        self.planter = Planter()

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        sleep(1)

        while not self.cancellation_token.is_cancelled:
            if not self.start_at_farm:
                if self.cancellation_token.is_cancelled:
                    break
                # # Equip staff
                equipstaff()

                if self.cancellation_token.is_cancelled:
                    break

                # # Recall
                # recall(self.cancellation_token)
                saferecall(self.cancellation_token)
                
                if self.cancellation_token.is_cancelled:
                    break

                # # Go to blacksmith
                gotoblacksmith_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # # Repair gear
                repairgear(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # # Recall again
                recall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # # Go to shop
                gotoshop_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # # Sell produce
                sellproduce(self.crop_type, self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # Buy seeds
                buyseeds(self.crop_type, self.num_seed_bags_per_hoe * self.num_hoes, self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # Move the seed bags to a different position in the inventory
                moveseeds(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # Recall back to farm
                recall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                # Eat some foodzies
                eat(self.cancellation_token, 2)

                if self.cancellation_token.is_cancelled:
                    break

                # Run to farm spot
                gotofarm_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break
            
            # Start at farm point
            self.start_at_farm = False
            iterations = ceil(self.num_seed_bags_per_hoe / 3)

            # Equip hoe
            # equiphoe(0)
            
            # Plant all seeds
            self.planter.plantall()

            while True:
                if self.cancellation_token.is_cancelled:
                    break

                # self.harvester.startharvest()
                
                sleep(1)

    def stop(self):
        self.cancellation_token.cancel()