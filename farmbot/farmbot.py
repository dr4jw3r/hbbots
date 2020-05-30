###########
from threading import Thread
from time import sleep
from math import ceil
###########
from lib.CancellationToken import CancellationToken
###########
from farmbot.common import *
from lib.common import *
from levelbot.levelbot_common import equipweapon
###########
from lib.threads.killaround import KillAroundThread

class FarmThread(object):
    def __init__(self, crop_type, start_at_farm):
        self.start_at_farm = start_at_farm
        self.crop_type = crop_type
        self.num_hoes = 4
        self.num_seed_bags_per_hoe = 9
        self.cancellation_token = CancellationToken()

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

            for hoe_index in range(self.num_hoes):
                hoe_equipped = False

                if self.cancellation_token.is_cancelled:
                    break

                for i in range(iterations):
                    # Ensure good spot
                    verifylocation(self.cancellation_token)

                    if self.cancellation_token.is_cancelled:
                        break

                    # equip hoe
                    hoe_equipped = equiphoe(hoe_index)
                    if not hoe_equipped:
                        hoe_index += 1

                        # break current iterations and move on to new hoe
                        break

                    if self.cancellation_token.is_cancelled:
                        break

                    # hoe equipped, plant seeds
                    has_planted = plantseeds(self.cancellation_token)

                    if self.cancellation_token.is_cancelled:
                        break

                    if has_planted:
                        harvest(self.cancellation_token, self.crop_type)

                        if self.cancellation_token.is_cancelled:
                            break

                        has_enemy = checkforenemies(self.cancellation_token)
                        if has_enemy:
                            # Check for enemies
                            equipweapon()
                            sleep(0.1)
                            kill_thread = KillAroundThread(singlescan=True, no_loot=True)
                            kill_thread.join()

                    else:
                        break

    def stop(self):
        self.cancellation_token.cancel()