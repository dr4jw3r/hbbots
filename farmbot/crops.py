from farmbot.Crop import Crop

CROPS = {
    "watermelon": Crop("watermelon", 36, "enter"),
    "garlic": Crop("garlic", 36, "enter"),
    "carrot": Crop("carrot", 36, "enter"),
    "corn": Crop("corn", 36, "click"),
    "bellflower": Crop("bellflower", 36, "enter"),
    "tomato": Crop("tomato", 36, "click"),
    "grapes": Crop("grapes", 36, "click"),
    "ginseng": Crop("ginseng", 36, "click")
}

def getcrop(crop_name):
    return CROPS[crop_name]