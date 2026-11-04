import sys
from PIL import Image
n, side, y0, y1, step = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
a = Image.open("n%s.jpg" % n)
f = a.size[0] / 701
x0, x1 = (12, 345) if side == "L" else (355, 690)
k, y = 0, y0
while y < y1:
    box = [int(x0 * f), int(y * f), int(x1 * f), int(min(y + step + 3, y1) * f)]
    a.crop(box).save("t%s%s_%02d.png" % (n, side, k))
    k, y = k + 1, y + step
print(k)
