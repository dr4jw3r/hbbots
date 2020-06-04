###########
from threading import Thread
from time import sleep, time
from math import ceil
###########
from lib.CancellationToken import CancellationToken
###########
from farmbot.common import *
from lib.common import *
from lib.LocationMonitor import LocationMonitor
from levelbot.levelbot_common import equipweapon
from farmbot.positions import FARM_WPTS
from farmbot.harvester import Harvester
from farmbot.planter import Planter
from farmbot.scanner import Scanner
from farmbot.drophandler import DropHandler
from farmbot.hoethread import HoeThread
###########
from lib.threads.killaround import KillAroundThread

class FarmThread(object):
    def __init__(self, crop_type, sell_mode, start_at_farm):
        self.start_at_farm = start_at_farm
        self.crop_type = crop_type
        self.sell_mode = sell_mode
        self.num_seed_bags = 36
        self.num_hoes = 4
        self.cancellation_token = CancellationToken()

        self.location_monitor = LocationMonitor()
        self.harvester = Harvester()
        self.planter = Planter()
        self.scanner = Scanner()
        self.drop_handler = DropHandler()
        self.hoe_thread = HoeThread()

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def enemyscan(self):
        has_enemy = self.scanner.scanenemy(self.cancellation_token)
        if has_enemy:
            kt = KillAroundThread(singlescan=True, no_loot=True)
            kt.join()
            sleep(0.1)

        return has_enemy

    def hoe(self, index):
        hoe_equipped = False
        while not hoe_equipped:
            hoe_equipped = equiphoe(index)

            if not hoe_equipped:
                if index + 1 == self.num_hoes:
                    index = 0
                else:
                    index += 1

        return index

    def run(self):
        sleep(1)        

        while not self.cancellation_token.is_cancelled:
            if not self.start_at_farm:
                if self.cancellation_token.is_cancelled:
                    break

                print("Equip staff")
                equipstaff()

                if self.cancellation_token.is_cancelled:
                    break

                print("Recall")
                recall(self.cancellation_token)
                
                if self.cancellation_token.is_cancelled:
                    break

                print("Go to blacksmith")
                gotoblacksmith_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Repair gear")
                repairgear(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Selling")
                sellitems(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Recall again")
                saferecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Go to shop")
                gotoshop_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Sell produce")
                sellproduce(self.crop_type, self.sell_mode, self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Buy seeds")
                buyseeds(self.crop_type, self.num_seed_bags, self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Move the seed bags to a different position in the inventory")
                moveseeds(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Recall back to farm")
                saferecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break

                print("Eat some foodzies")
                eat(self.cancellation_token, 2)

                if self.cancellation_token.is_cancelled:
                    break

                print("Run to farm spot")
                gotofarm_fromrecall(self.cancellation_token)

                if self.cancellation_token.is_cancelled:
                    break
            
            print("Start at farm point")
            self.start_at_farm = False
            hoe_index = 0

            verifylocation(self.cancellation_token)
            
            hoe_timer = time()
            timeout_timer = time()
            scan_time = time()
            enemy_time = time()
            finish_time = time()
            seedbag_condition = False
            moved_produce = False

            print("Equip hoe")
            hoe_index = self.hoe(hoe_index)
            s_t = time()
            while True:              
                if time() - timeout_timer >= 900:
                    print("Broke out with timeout")
                    break

                bag_pos = self.planter.findseedbag()
                if bag_pos[0] == -1:
                    print("No more seedbags")
                    seedbag_condition = True

                current_time = time()
                self.harvester.startharvest()

                sleep(1)

                if self.cancellation_token.is_cancelled:
                    break

                # every 1 seconds check
                if current_time - scan_time >= 1:
                    replant = self.scanner.scan()

                    if any(replant):
                        self.harvester.stopharvest()

                        coords = self.location_monitor.getcoordinates()
                        if coords[0] != FARM_WPTS[-1][0] or coords[1] != FARM_WPTS[-1][1]:
                            verifylocation(self.cancellation_token)

                        self.planter.replant(replant)
                    
                    scan_time = time()

                # broken somehow
                if self.hoe_thread.ishoebroken() or time() - hoe_timer >= 30:
                    print("Hoe broke")
                    self.harvester.stopharvest()
                    hoe_index = self.hoe(hoe_index)
                    self.hoe_thread.acknowledge()
                    hoe_timer = time()                                        

                if current_time - enemy_time >= 10:                    
                    if self.enemyscan():
                        hoe_index = self.hoe(hoe_index)
                    enemy_time = time()

                # after 5 minutes harvest all
                # 780 = 13 mins (15 min despawn?)
                if (current_time - finish_time >= 780) or seedbag_condition:
                    print("Finish timer. Seedbag: ", seedbag_condition)
                    finish_time = time()
                    for i in range(4):
                        replant = self.scanner.scan()
                        for i in range(len(replant)):
                            if not replant[i]:
                                self.harvester.harvestsingle(i, self.hoe_thread, hoe_index, self.cancellation_token)
                        
                        sleep(0.1)
                    
                    # check for drops here (organised left to right)
                    self.harvester.stopharvest()
                    self.drop_handler.pickup(self.crop_type, self.cancellation_token)                    
                    moveproduce(self.crop_type)
                    
                    if not seedbag_condition:
                        if self.enemyscan():
                            hoe_index = self.hoe(hoe_index)
                
                if seedbag_condition:
                    break

            self.harvester.stopharvest()
            print("Elapsed time: ", time() - s_t)
            self.hoe_thread.stop()
            self.enemyscan()
                
    def stop(self):
        self.cancellation_token.cancel()
        self.hoe_thread.stop()
        self.location_monitor.stop()