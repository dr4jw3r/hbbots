from PIL import Image
from time import time 

num_pixels = 32*32
step = 100 / num_pixels

start = time()

sample0 = Image.open("./sample_0.png").convert('LA')
pixels0 = sample0.load()


for i in range(5):
    sample1 = Image.open("./sample_n" + str(i) + ".png").convert('LA')
    pixels1 = sample1.load()

    score = 0

    for y in range(32):
        for x in range(32):
            if pixels0[x, y] == pixels1[x, y]:
                score += step

    print(score)

end = time()
elapsed = end - start
print("Elapsed: ", elapsed)