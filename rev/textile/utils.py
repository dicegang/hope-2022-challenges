class Rng:
    def __init__(self, seed=0x51c3):
        self.state = seed

    def get(self):
        self.state *= 75
        assert self.state < (1<<31)
        self.state += 74
        assert self.state < (1<<31)
        self.state %= 0x10001
        return self.state


if __name__ == '__main__':
    rng = Rng()
    while True:
        print(rng.get())
        input()
