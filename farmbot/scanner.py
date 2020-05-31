from time import sleep, time
from lib.inputcontrol import moveto
from lib.imagesearch import imagesearcharea, region_grabber

from farmbot.positions import TEST_BOX_SIZE, TEST_BOX_POSITIONS, DROP_BOX_POSITIONS, DROP_BOX_SIZE, ENEMY_SCAN_POSITIONS

class Scanner(object):
    def __init__(self):
        self.CURSOR_IMAGE = "./common/samples/misc/cursor.png"
        self.CURSOR_PRECISION = 0.4427884615384618
        self.CROP_STAGE_PRECISION = 0.4
        self.CROP_STAGE_IMAGES = [
            (1, "./common/samples/produce/crop_1.png"),
            (2, "./common/samples/produce/crop_2.png"),
            (3, "./common/samples/produce/crop_3.png")
        ]

    def getcropstage(self, position):
        moveto((400, 600))
        sleep(0.05)

        x2 = position.x + TEST_BOX_SIZE[0]
        y2 = position.y + TEST_BOX_SIZE[1]

        img = region_grabber((position.x, position.y, x2, y2))
        # img.save("cropstage_" + str(time()) + ".png")

        for stage in self.CROP_STAGE_IMAGES:
            crop_pos = imagesearcharea(stage[1], -1, -1, -1, -1, im=img, precision=self.CROP_STAGE_PRECISION)
            
            if crop_pos[0] != -1:
                return stage[0]

        return -1

    def scan(self):
        replant = [False, False, False]        

        for i in range(len(TEST_BOX_POSITIONS)):
            position = TEST_BOX_POSITIONS[i]
            crop_stage = self.getcropstage(position)
            
            if crop_stage == -1:
                replant[i] = True

        return replant

    def scanenemy(self, cancellation_token):
        SIZE = 40        
        #  add token
        for pos in ENEMY_SCAN_POSITIONS:
            x1 = pos.x - (SIZE/2)
            y1 = pos.y - (SIZE/2)
            x2 = pos.x + (SIZE/2)
            y2 = pos.y + (SIZE/2)

            moveto((pos.x, pos.y))
            sleep(0.08)
            cursor = imagesearcharea(self.CURSOR_IMAGE, x1, y1, x2, y2, precision=self.CURSOR_PRECISION)
            if cursor[0] != -1:
                return True

        return False

    def scandrops(self, crop_type):
        image_path = "./common/samples/produce/" + crop_type + ".png"

        moveto((400, 600))
        sleep(0.05)
        
        has_drop = [False] * len(DROP_BOX_POSITIONS)
        for i in range(len(DROP_BOX_POSITIONS)):
            pos = DROP_BOX_POSITIONS[i]
            x2 = pos.x + DROP_BOX_SIZE[0]
            y2 = pos.y + DROP_BOX_SIZE[1]

            drop_pos = imagesearcharea(image_path, pos.x, pos.y, x2, y2, precision=0.7, save=True, name=str(time()))
            if drop_pos[0] != -1:
                has_drop[i] = True

        return [has_drop[1], has_drop[0], has_drop[2]]