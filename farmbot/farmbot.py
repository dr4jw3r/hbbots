import logging
import inspect
###########
from threading import Thread
from time import sleep, time
###########
from core import configurationparser
###########
from lib.utils.CancellationToken import CancellationToken
from lib.utils.ScreenshotThread import ScreenshotThread
from lib.utils.TimekeeperThread import TimekeeperThread
###########
from lib.waypoints import WAYPOINTS
###########
from lib.actions import eat
from lib.equipment import equipstaff, equiphoe, equipweapon
from lib.inventory import closeinventory
from lib.spells import recall
from lib.ocr import OCR
from lib.Movement import Movement
from lib.utils.Scanner import Scanner
from lib.threads.killaround import KillAroundThread
###########
from lib.monitor.LocationMonitor import LocationMonitor
from lib.monitor.HealthMonitor import HealthMonitor
###########
from lib.npc.blacksmith import gotoblacksmith, repair
from lib.npc.shopkeeper import gotoshop, sellproduce, buyseeds
###########
from farmbot.BotState import BotState
from farmbot.HoeMonitor import HoeMonitor
from farmbot.CropMonitor import CropMonitor
from farmbot.BagMonitor import BagMonitor
from farmbot.CursorMonitor import CursorMonitor
from farmbot.Planter import Planter
from farmbot.Harvester import Harvester
from farmbot.DropHandler import DropHandler
from farmbot.InventoryManager import InventoryManager
from farmbot.crops import getcrop

class FarmThread(object):
    def __init__(self, start_at_farm):
        # variables
        self.start_at_farm = start_at_farm

        crop_name = configurationparser.readconfig()["FARMBOT"]["Crop"]
        self.crop = getcrop(crop_name)

        self.num_hoes = 4
        self.pausing_authority = None
        self.waypoints = None

        self.cancellation_token = CancellationToken()
        self.logger = logging.getLogger("hbbot.farmbot.main")        

        # threads that need to be stopped
        self.screenshot_thread = ScreenshotThread(self.cancellation_token)
        self.location_monitor = LocationMonitor(self.screenshot_thread, self.cancellation_token) 

        # utils
        self.state = BotState()
        self.ocr = OCR(self.screenshot_thread)
        self.scanner = Scanner(self.screenshot_thread, self.cancellation_token)
        self.movement = Movement(self.location_monitor, self.cancellation_token)
        self.planter = Planter(self.screenshot_thread, self.cancellation_token)
        self.drop_handler = DropHandler(self.crop, self.screenshot_thread)
        self.inventory_manager = InventoryManager(self.scanner, self.crop, self.cancellation_token)

        self.timekeeper = TimekeeperThread(self.cancellation_token)
        harvest_time_timeout = int(configurationparser.readconfig()["FARMBOT"]["HarvestTimeout"])
        self.timekeeper.register(self.__harvesttimecallback, harvest_time_timeout)
        self.timekeeper.register(self.__timeoutcallback, 1000)

        self.hoe_monitor = HoeMonitor(self.screenshot_thread, self.state, self.cancellation_token)
        self.hoe_monitor.subscribe(self.__hoecallback)
        
        self.bag_monitor = BagMonitor(self.ocr, self.scanner, self.cancellation_token)
        self.bag_monitor.subscribe(self.__bagcallback)

        self.crop_monitor = CropMonitor(self.screenshot_thread, self.cancellation_token)

        self.health_monitor = HealthMonitor(self.ocr, self.cancellation_token)
        self.health_monitor.subscribe(self.__healthcallback)

        self.cursor_monitor = CursorMonitor(self.screenshot_thread, self.cancellation_token)

        self.harvester = Harvester(self.crop_monitor, self.ocr, self.state)

        # run the thread
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    # Utility functions

    def __pause(self, authority, force=False):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        self.logger.debug("__pause " + calframe[1][3])

        if self.pausing_authority is None or force is True:
            self.pausing_authority = authority

            self.harvester.stopharvest()
            self.crop_monitor.pause()
            self.hoe_monitor.pause()
            self.bag_monitor.pause()
            self.health_monitor.pause()
            self.cursor_monitor.pause()

            return True

        return False

    def __resume(self, authority, force=False):        
        if authority == self.pausing_authority or force:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            self.logger.debug("__resume " + calframe[1][3])
            self.harvester.startharvest()
            self.hoe_monitor.resume()
            self.bag_monitor.resume()
            self.crop_monitor.resume(0.25)
            self.health_monitor.resume()
            self.cursor_monitor.resume()
            self.pausing_authority = None

    def __cleanup(self):
        threads = [
            self.hoe_monitor,
            self.crop_monitor,
            self.timekeeper,
            self.bag_monitor,
            self.health_monitor,
            self.cursor_monitor
        ]
        
        self.harvester.stopharvest()
        
        for t in threads:
            t.stop()
            t.join()        

    def __reset(self):
        self.pausing_authority = None
        self.timekeeper.reset()
        self.crop_monitor.unsubscribe(self.__harvestallcallback)
        self.crop_monitor.subscribe(self.__cropcallback)

    def __getlocation(self):
        if self.waypoints is None:
            coordinates = None
        
            while coordinates is None:
                if self.cancellation_token.is_cancelled:
                    return

                coordinates = self.location_monitor.getcoordinates()
            
            self.waypoints = WAYPOINTS["planting_spot"]
            self.waypoints.append([coordinates, 0])

    # Action functions

    def __blacksmith(self):
        self.logger.debug("going to blacksmith")
        gotoblacksmith(self.movement, self.scanner, self.cancellation_token)

        if self.cancellation_token.is_cancelled:
            return

        self.logger.debug("repairing gear")
        repair(self.movement, self.scanner, self.cancellation_token)
        self.state.sethoeindex(0)

    def __shop(self):
        self.logger.debug("going to shop")
        gotoshop(self.movement, self.scanner)

        self.logger.debug("selling produce")
        sellproduce(self.crop, self.scanner, self.cancellation_token)

        self.logger.debug("buying seeds")
        buyseeds(self.crop, self.scanner, self.movement, self.cancellation_token)

    def __farm(self):        
        sleep(1)    
        
        if not self.start_at_farm:
            self.logger.debug("equipping staff")

            if self.cancellation_token.is_cancelled:
                return

            equipstaff()

            if self.cancellation_token.is_cancelled:
                return

            closeinventory()

            if self.cancellation_token.is_cancelled:
                return

            sleep(2)

            self.logger.debug("recalling (first)")
            recall(self.cancellation_token)

            if self.cancellation_token.is_cancelled:
                return

            self.__blacksmith()

            if self.cancellation_token.is_cancelled:
                return

            self.logger.debug("recalling (second)")
            recall(self.cancellation_token)

            if self.cancellation_token.is_cancelled:
                return

            self.__shop()

            if self.cancellation_token.is_cancelled:
                return

            self.logger.debug("recalling (third)")
            recall(self.cancellation_token)

            if self.cancellation_token.is_cancelled:
                return

            self.logger.debug("eating")
            eat(1, self.cancellation_token)
            
            self.logger.debug("going to planting spot")
            self.movement.followwaypoints(self.waypoints)
        
            if self.cancellation_token.is_cancelled:
                return

        self.start_at_farm = False

        self.logger.debug("getting location")
        self.__getlocation()        

        if self.cancellation_token.is_cancelled:
            return

        self.logger.debug("going to planting spot 2")
        self.movement.gotolastwaypoint(self.waypoints)

        if self.cancellation_token.is_cancelled:
            return

        self.logger.debug("picking up drops")
        self.drop_handler.pickup(self.cancellation_token)

        if self.cancellation_token.is_cancelled:
            return

        self.__reset()
        hoe_equipped = False
        while not hoe_equipped:
            if self.cancellation_token.is_cancelled:
                return

            hoe_equipped = equiphoe(self.state.gethoeindex(), self.ocr)
            if not hoe_equipped:
                self.state.incrementhoeindex()

        self.harvester.startharvest()
        self.crop_monitor.start()
        self.hoe_monitor.start(10)
        self.health_monitor.start() 
        self.bag_monitor.start()
        self.cursor_monitor.start()
        self.timekeeper.start()

    # Callbacks

    def __hoecallback(self, payload, args):
        if self.__pause("hoemonitor"):
            self.logger.debug("hoe callback")
            self.state.incrementhoeindex()
            equiphoe(self.state.gethoeindex(), self.ocr)
            self.__resume("hoemonitor")

    def __cropcallback(self, payload, args):
        if self.__pause("cropmonitor"):
            self.crop_monitor.useprecisions("normal")
            self.logger.debug("crop callback")
            for i in range(2):
                current = self.location_monitor.getcoordinates()
                if current is not None:
                    last_wpt = self.waypoints[-1][0]
                    if current[0] != last_wpt[0] or current[1] != last_wpt[1]:
                        self.movement.gotolastwaypoint(self.waypoints)
                        sleep(1)

            self.planter.replant(payload["replant"])
            self.__resume("cropmonitor")

    def __harvestallcallback(self, payload, args):
        replant = payload["replant"]
        needs_harvest = [False] * len(replant)
        for i in range(len(replant)):
            needs_harvest[i] = not replant[i]

        order = [1, 0, 2]
        for o in order:
            if needs_harvest[o]:
                self.harvester.moveto(o)
                self.harvester.startharvest(move=False)
                break

        if not any(needs_harvest):
            self.__pause("harvestdone", True)
            self.harvester.stopharvest()
            self.drop_handler.pickup(self.cancellation_token)
            self.inventory_manager.moveproduce()

            if args is None or not args["intermediate"]:
                self.__farm()
            else:
                self.crop_monitor.unsubscribe(self.__harvestallcallback)
                self.crop_monitor.subscribe(self.__cropcallback)
                self.__resume("harvestdone", True)

    def __bagcallback(self, payload, args):
        if self.__pause("bagmonitor", True):
            self.logger.debug("bag callback")
            self.timekeeper.pause()

            self.state.sethoeindex(self.num_hoes - 1)
            equiphoe(self.state.gethoeindex(), self.ocr)

            self.crop_monitor.unsubscribe(self.__cropcallback)
            self.crop_monitor.subscribe(self.__harvestallcallback)
            self.crop_monitor.useprecisions("harvestall")
            self.crop_monitor.resume(0.25)
            self.health_monitor.resume()
            self.harvester.startharvest()

    def __healthcallback(self, payload, args):
        if self.__pause("healthmonitor"):
            self.logger.debug("health callback")
            equipweapon()
            t = KillAroundThread(self.ocr, singlescan=True, no_loot=True)
            t.join()
            sleep(0.2)
            equiphoe(self.state.gethoeindex(), self.ocr)
            self.__resume("healthmonitor")

    def __harvesttimecallback(self):
        if self.__pause("harvesttime", True):
            self.logger.debug("harvest time callback")

            self.crop_monitor.unsubscribe(self.__cropcallback)
            self.crop_monitor.subscribe(self.__harvestallcallback, {"intermediate": True})
            self.crop_monitor.useprecisions("harvestall")
            self.crop_monitor.resume(0.25)
            self.harvester.startharvest()       

            self.__resume("harvesttime")

    def __cursorcallback(self, payload, args):
        if self.__pause("cursormonitor"):
            self.logger.debug("cursor monitor callback")
            equipweapon()
            t = KillAroundThread(self.ocr, singlescan=True, no_loot=True)
            t.join()
            sleep(0.1)
            equiphoe(self.state.gethoeindex(), self.ocr)
            self.__resume("cursormonitor")

    def __timeoutcallback(self):
        if self.__pause("timeoutcallback", True):
            self.logger.debug("timeout callback")
            sleep(5)
            self.__farm()

    # Main functions

    def run(self):
        self.logger.debug("started")
        self.__farm()
               
    def stop(self):
        self.cancellation_token.cancel()
        self.__cleanup()
        self.thread.join()
        self.logger.debug("stopped")