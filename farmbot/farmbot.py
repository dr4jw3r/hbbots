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
from farmbot.scanner import Scanner
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
        self.scanner = Scanner()

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
            scan_time = time()
            finish_time = time()

            while True:
                current_time = time()
                self.harvester.startharvest()

                sleep(1)

                if self.cancellation_token.is_cancelled:
                    break

                # every 2 seconds check
                if current_time - scan_time >= 1:
                    self.harvester.stopharvest()
                    replant = self.scanner.scan()
                    self.planter.replant(replant)
                    scan_time = time()

                # after 4 minutes harvest all
                # 240
                if current_time - finish_time >= 10:
                    replant = self.scanner.scan()
                    for i in range(len(replant)):
                        if not replant[i]:
                            self.harvester.harvestsingle(i, self.cancellation_token)
                    
                    # check for drops here
                    self.scanner.scandrops(self.crop_type)

                    finish_time = time()

                self.harvester.stopharvest()
                
    def stop(self):
        self.cancellation_token.cancel()