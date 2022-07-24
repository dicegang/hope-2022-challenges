from matplotlib import pyplot as plt
import random
import math
from scipy.spatial import ConvexHull
from tqdm import tqdm

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
flag = "hope{CPYTHON_ISjvmV2}"
assert len(flag) == len(set(flag))
print(len(flag))

# for s in tqdm(range(10000000)):

random.seed(11787)
rad = 50

pts = []
for c in charset:
    r = math.sqrt(random.random()) * rad
    t = random.random() * 2 * math.pi
    pts.append((round(r * math.cos(t)), round(r * math.sin(t))))

hull = ConvexHull(pts)
# print(pts)
print(len(hull.vertices))
deet = set(charset)
m = {}
for (a, b) in zip(hull.vertices, flag):
    m[b] = pts[a]
    deet.remove(b)
for i in range(len(pts)):
    if i not in hull.vertices:
        c = random.choice(list(deet))
        deet.remove(c)
        m[c] = pts[i]

# sort the keys
m = {k: m[k] for k in charset}
print(m)

# plt.plot([p[0] for p in pts], [p[1] for p in pts], marker=".", linestyle="None")
# plt.plot(
#     [pts[v][0] for v in list(hull.vertices) + [hull.vertices[0]]],
#     [pts[v][1] for v in list(hull.vertices) + [hull.vertices[0]]],
#     linestyle="--",
#     color="r",
# )
# plt.xlim((-50, 50))
# plt.ylim((-50, 50))
# plt.show()
