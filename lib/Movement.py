import logging
#
from time import sleep, time
# 
from lib.inputcontrol import rightdown, rightup, moveto, click, clickright
from lib.spells import recall
from lib.equipment import equipstaff
from lib.inventory import closeinventory

class Movement(object):
    def __init__(self, location_monitor, cancellation_token):
        self.logger = logging.getLogger("hbbot.lib.movement")
        self.location_monitor = location_monitor
        self.cancellation_token = cancellation_token

        self.GRID_SQUARE_SIZE = (32, 32)
        self.SQUARES = { "x": 25, "y": 17 }

        self.direction_x = 0
        self.direction_y = 0
        self.distance_x = 0        
        self.distance_y = 0

    def __reset(self):
        self.direction_x = 0
        self.direction_y = 0
        self.distance_x = 0        
        self.distance_y = 0

    def __middleloc(self):        
        x = int((self.SQUARES["x"] / 2) * self.GRID_SQUARE_SIZE[0])
        y = int((self.SQUARES["y"] / 2) * self.GRID_SQUARE_SIZE[1])

        return (x, y)

    def __parselocation(self, point, current_point):
        direction_x = 1 if current_point[0] < point[0] else -1
        direction_y = 1 if current_point[1] < point[1] else -1
        distance_x = abs(current_point[0] - point[0])
        distance_y = abs(current_point[1] - point[1])
        return (direction_x, direction_y, distance_x, distance_y)

    def __gotopoint(self, point, tolerance, locationstop):
        timeout_time = 35
        timeout_timer = time()

        while True:
            if self.cancellation_token.is_cancelled:
                return False

            if time() - timeout_timer > timeout_time:
                sleep(0.1)
                equipstaff()
                sleep(0.1)
                recall(self.cancellation_token)
                sleep(0.2)
                return False

            current_point = self.location_monitor.getcoordinates()
            current_location = self.location_monitor.getlocation()

            if locationstop is not None and current_location is not None:
                if current_location.lower().find(locationstop.lower()) != -1:
                    self.logger.debug("locationstop reached")
                    moveto((400, 600))
                    sleep(0.05)
                    clickright()
                    self.__reset()
                    return True

            if current_point is not None:
                (self.direction_x, self.direction_y, self.distance_x, self.distance_y) = self.__parselocation(point, current_point)        

                x_within = self.distance_x  <= tolerance
                y_within = self.distance_y <= tolerance

                if x_within and y_within:
                    self.logger.debug("point reached")
                    moveto((400, 600))
                    sleep(0.05)
                    clickright()
                    self.__reset()
                    return True

            middle = self.__middleloc()
            x = middle[0] + self.GRID_SQUARE_SIZE[0] * (self.distance_x * self.direction_x)
            y = middle[1] + self.GRID_SQUARE_SIZE[1] + (self.distance_y * self.direction_y * self.GRID_SQUARE_SIZE[1])

            # to not click on menu
            if y > self.GRID_SQUARE_SIZE[1] * self.SQUARES["y"]:
                y = self.GRID_SQUARE_SIZE[1] * self.SQUARES["y"]

            # to not click on char
            if x > 380 and x < 420:
                if y < 310 and y > 250:
                    y = 240

            # to not click on minimap
            if x > 600:
                x = 600

            moveto((x, y))
            sleep(0.1)
            click()

            if self.distance_x > 5 or self.distance_y > 5:
                sleep(1.5)
            else:
                sleep(1)

    def followwaypoints(self, waypoints, locationstop=None):
        closeinventory()

        for waypoint in waypoints:
            if self.cancellation_token.is_cancelled:
                break

            point = waypoint[0]
            tolerance = waypoint[1]

            reached = self.__gotopoint(point, tolerance, locationstop)
            
            if not reached:
                self.followwaypoints(waypoints, locationstop)
                break

        
    def gotolastwaypoint(self, waypoints, locationstop=None):
        waypoint = waypoints[-1]
        point = waypoint[0]
        tolerance = waypoint[1]
        self.__gotopoint(point, tolerance, locationstop)
    