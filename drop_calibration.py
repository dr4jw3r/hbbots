from os import listdir
from lib.imagesearch import imagesearch_withinimage
from PIL import Image

DROPS = [
    ("bodice",          0.7, True),
    ("cap",             0.7, True),
    ("falchion",        0.7, True),
    ("falchion2",       0.7, True),
    ("falchion3",       0.7, True),
    ("fullhelm",        0.8, True),
    ("gladius",         0.7, True),
    ("mallet",          0.7, True),
    ("ring",            0.72, False),
    ("saxonaxe",        0.7, True),
    ("scutum",          0.7, True),
    ("shirtM",          0.7, True),
    ("shirtW",          0.7, True),
    ("targeshield",     0.7, True),
    ("tomahawk",        0.7, True),
    ("trousersM",       0.7, True),
    ("trousersW",       0.8, True),
    ("tunic",           0.7, True),
    ("wand",            0.7, True),
    ("wand2",           0.7, True),
    ("wand3",           0.7, True),
    ("wizardhat",       0.8, True),
    ("woodshield",      0.65, True),
    ("zem",             0.85, True),
    ("zem2",            0.8, True),
    # ==================
    # BODY PARTS
    # ==================
    ("slimejelly",      0.7, True),
    ("snakeskin",       0.50, True),
    # ("snakemeat",       0.8, False),
    ("snaketeeth",      0.85, True),
    ("snaketongue",     0.53, True),
    ("antlegs",         0.8, True),
    ("antantenna",      0.7, True),
    ("scorpionpincer", 0.7, True),
    ("scorpionskin",    0.7, True),
    ("scorpionsting",   0.7, True)
]

def stringify_drop(drop):
    return "(\"{0}\",\t\t\t{1}, {2})".format(drop[0], drop[1], drop[2])

SAMPLES_DIR = "./calibration_samples"
SAMPLES = []
PROCESSED = []

for sample in listdir(SAMPLES_DIR):
    SAMPLES.append(Image.open(SAMPLES_DIR + "/" + sample))

for i in range(len(DROPS)):
    drop = DROPS[i]
    target = "./common/samples/drops/" + drop[0] + ".png"
    results = []
    
    for sample in SAMPLES:
        precision = 0.01
        pos = [0, 0]

        while pos[0] != -1:
            pos = imagesearch_withinimage(sample, target, precision)
            precision += 0.01
            
        results.append(precision)

    average = (sum(results) / len(results)) + 0.18
    PROCESSED.append((DROPS[i][0], average, DROPS[i][2]))

with open("./lib/drops.py", "w") as f:
    f.write("DROPS = [\n")

    for drop in PROCESSED:
        f.write("\t{0},\n".format(stringify_drop(drop)))        

    f.write("]")