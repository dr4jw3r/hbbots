from os import listdir
from time import sleep, time
from cv2 import imread, imwrite
from lib.inputcontrol import moveto
from lib.imagesearch import imagesearcharea, imagesearcharea2, region_grabber

from farmbot.positions import TEST_BOX_SIZE, TEST_BOX_POSITIONS, DROP_BOX_POSITIONS, DROP_BOX_SIZE, ENEMY_SCAN_POSITIONS, SCAN_CURSOR_POSITIONS

class Scanner(object):
    def __init__(self):
        self.CURSOR_IMAGE = "./common/samples/misc/cursor.png"
        self.CURSOR_PRECISION = 0.4427884615384618
        self.CROP_STAGE_PRECISION = {
            "mid": 0.65,
            "left": 0.65,
            "right": 0.75
        }
        self.CROP_IMAGES = self._loadimages()

    def _loadimages(self):
        crop_images = {}
        IMAGES_DIR = "./common/samples/produce/crops/"
        for sample in listdir(IMAGES_DIR):
            crop_images[sample] = imread(IMAGES_DIR + sample, 0)

        return crop_images

    def getcropstageold(self, position):
        CROP_STAGE_PRECISION = 0.62
        CROP_STAGE_IMAGES = [
            (1, imread("./common/samples/produce/crop_1.png", 0)),
            (2, imread("./common/samples/produce/crop_2.png", 0)),
            (3, imread("./common/samples/produce/crop_3.png", 0))
        ]
        CROP_STAGE_GLOW_IMAGES = [
            (1, imread("./common/samples/produce/crop_1_glow.png", 0)),
            (2, imread("./common/samples/produce/crop_2_glow.png", 0)),
            (3, imread("./common/samples/produce/crop_3_glow.png", 0))
        ]
        x2 = position.x + TEST_BOX_SIZE[0]
        y2 = position.y + TEST_BOX_SIZE[1]

        img = region_grabber((position.x, position.y, x2, y2))
        # img.save("cropstage_" + str(time()) + ".png")

        for stage in CROP_STAGE_IMAGES:
            (crop_pos, max_val, sample) = imagesearcharea2(stage[1], im=img, precision=CROP_STAGE_PRECISION)
            
            if crop_pos[0] != -1:
                return stage[0]

        for stage in CROP_STAGE_GLOW_IMAGES:
            (crop_pos, max_val, sample) = imagesearcharea2(stage[1], im=img, precision=CROP_STAGE_PRECISION)
            
            if crop_pos[0] != -1:
                return stage[0]

        # print("Crop Not Found: ", max_val)
        # sample.save("./ps/{0}_{1}.png".format(max_val, time()))
        return -1

    def getcropstage(self, index):
        position = TEST_BOX_POSITIONS[index]
        x2 = position.x + TEST_BOX_SIZE[0]
        y2 = position.y + TEST_BOX_SIZE[1]

        img = region_grabber((position.x, position.y, x2, y2))

        box_position = None
        if index == 0:
            box_position = "mid"
        elif index == 1:
            box_position = "left"
        else:
            box_position = "right"

        test_images = []
        for i in range(1, 4):
            template = self.CROP_IMAGES["crop_{0}_{1}.png".format(i, box_position)]
            (crop_pos, max_val, sample) = imagesearcharea2(template, im=img, precision=self.CROP_STAGE_PRECISION[box_position])

            if crop_pos[0] != -1:
                # sample.save("./ps/falsepos/{0}_{1}.png".format(max_val, time()))
                return i

            template = self.CROP_IMAGES["crop_{0}_{1}_glow.png".format(i, box_position)]
            (crop_pos, max_val, sample) = imagesearcharea2(template, im=img, precision=self.CROP_STAGE_PRECISION[box_position])

            if crop_pos[0] != -1:
                # sample.save("./ps/falsepos/{0}_{1}.png".format(max_val, time()))
                return i

        # sample.save("./ps/falseneg/{0}_{1}.png".format(max_val, time()))
        # img.save("./ps/img_{0}_{1}.png".format(max_val, time()))
        return -1

    def scan(self):
        replant = [False, False, False]                    

        for i in range(len(TEST_BOX_POSITIONS)):
            crop_stage = self.getcropstage(i)

            if crop_stage == -1:
                replant[i] = True

        return replant

    def scanenemy(self, cancellation_token):
        SIZE = 80        
        for pos in ENEMY_SCAN_POSITIONS:
            if cancellation_token.is_cancelled:
                return False

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

            drop_pos = imagesearcharea(image_path, pos.x, pos.y, x2, y2, precision=0.7)
            if drop_pos[0] != -1:
                has_drop[i] = True

        return [has_drop[1], has_drop[0], has_drop[2]]