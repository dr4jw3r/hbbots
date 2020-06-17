from farmbot.Crop import Crop

CROPS = {
    "watermelon": Crop("watermelon", 36, "enter", (10, 10)),
    "garlic": Crop("garlic", 36, "enter", (10, 10)),
    "carrot": Crop("carrot", 36, "enter", (10, 10)),
    "corn": Crop("corn", 36, "click", (10, 10)),
    "bellflower": Crop("bellflower", 36, "enter", (10, 10)),
    "tomato": Crop("tomato", 36, "click", (10, 10)),
    "grapes": Crop("grapes", 36, "click", (10, 10)),
    "bluegrapes": Crop("bluegrapes", 36, "click", (10, 10)),
    "mushroom": Crop("mushroom", 36, "enter", (10, 10)),
    "ginseng": Crop("ginseng", 36, "click", (18, 18)),
}

def getcrop(crop_name):
    return CROPS[crop_name]