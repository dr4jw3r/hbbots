from lib.imagesearch import region_grabber
from time import sleep

sleep(5)

p = (352, 320)
s = (32, 32)

r = (p[0], p[1], p[0] + s[0], p[1] + s[1])


for i in range(5):
    img = region_grabber(r)
    img.save("sample_n" + str(i) + ".png")
    sleep(1)