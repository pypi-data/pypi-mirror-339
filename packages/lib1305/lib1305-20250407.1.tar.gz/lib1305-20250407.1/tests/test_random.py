from lib1305 import poly1305
import os


def test_random():
    k = os.urandom(32)
    m = os.urandom(128)
    a = poly1305.auth(m, k)
    poly1305.verify(a, m, k)


if __name__ == 'main':
    test_random()
