

# There's probably a bunch of unused functions here... but they might be useful later.

import math

epsilon = 0.000001

def sign(n):
    return -1 if n < 0 else 1

def clamp(n, a, b):
    return min(max(n, a), b)

def clamp_1(n):
    return min(max(n, -1), 1)

def clamp_abs(n, a):
    return min(max(n, -a), a)

def clamp_01(n):
    return min(max(n, 0), 1)

# Used to precent division by zero errors
def not_zero(n):
    return n if abs(n) > epsilon else epsilon * sign(n)

def lerp(a, b, n):
    return (a * (n - 1) + b * n)

# Used by aerial turn controller
def correct(target, val, mult = 1):
    rad = constrain_pi(target - val)
    return (rad * mult)

def constrain_pi(n):
    while n > math.pi:
        n -= math.pi * 2
    while n < -math.pi:
        n += math.pi * 2
    return n

