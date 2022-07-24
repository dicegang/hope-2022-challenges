from sage.all import *

with open("ciphertext.txt", "r") as f:
	c = int(f.read(), 10)

m = b"hope{test-flag-plz-ignore}"
m = int.from_bytes(m, "little")

primes = primes_first_n(10000)[-1000:]
# mostly guarantees the dlog will exist, except for the 2 factor I think
primes = [p for p in primes if GF(p)(m).multiplicative_order() == (p-1)]
log_pi = RR(log(primes[0]) / log(2))
num_primes = ceil(2048 / 2 / log_pi)

def sample_pm1_smooth_prime(primes, num_primes):
    while True:
        pis = sample(primes, num_primes)
        p = 2 * prod(pis) + 1
        if is_prime(p):
            return p, pis
    

while True:
	try:
		p, pis = sample_pm1_smooth_prime(primes, num_primes)
		q, qis = sample_pm1_smooth_prime(set(primes) - set(pis), num_primes)

		"""
		sage automatically factors p-1 when calling log(), which is very fast
		so we don't even need to manually do the CRT and pollard's rho
		"""
		e_p = GF(p)(c).log(m)
		e_q = GF(q)(c).log(m)

		e = CRT([e_p, e_q], [p-1, q-1])
		n = p * q

		break

	except:
		pass

assert pow(m,e,n) == c


print(f"p = {p}")
print(f"q = {q}")
print(f"e = {e}")
