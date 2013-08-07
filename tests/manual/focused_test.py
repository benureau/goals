from toolbox import color
import testenv

from goals.explorer.motor import focused

babble = focused.FocusedMotorBabble((-1,), ((0.0, 10.0),), burst_length = 2, near_ratio = 100)

def f(x):
    if 4.0 < tuple(x)[0] < 5.0:
        return x
    if 9.0 < tuple(x)[0] < 10.0:
        return x
    else:
        return (0,)

for i in range(100):
    order = babble.babble()
    effect = f(order)
    babble.add_order(order, effect)
    c = color.red if tuple(effect)[0] != 0 else color.end
    print "{:5.2f} -> {}{:5.2f}{} ({})".format(tuple(order)[0], c, tuple(effect)[0], color.end, babble.burst)