from Crypto.Util.number import *
from tqdm import tqdm

exec(open('../output.txt').read())

def resultant(f1, f2, var):
    return Matrix(f1.sylvester_matrix(f2, var)).determinant()

pgcd = lambda g1, g2: g1.monic() if not g2 else pgcd(g2, g1%g2)

P.<y, k> = PolynomialRing(Zmod(n))
p1 = x * y^2 - enc[0]
p2 = (y + k)^2 - enc[1]
p3 = resultant(p1, p2, y)
k = min(p3.univariate_polynomial().monic().small_roots())

P.<y> = PolynomialRing(Zmod(n))
p1 = x * y^2 - enc[0]
p2 = (y + k)^2 - enc[1]
p4 = pgcd(p1, p2)
y = n - p4.coefficients()[0]

flag = 0
P.<k> = PolynomialRing(Zmod(n))

for c in tqdm(enc[::-1]):
    flag <<= 1
    poly = x * (y+k)^2 - c
    if len(poly.monic().small_roots()):
        flag += 1

print(flag)
print(long_to_bytes(flag))