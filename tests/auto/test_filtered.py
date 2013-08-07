import testenv
import treedict

from goals.explorer import effect

def test_belongs():
    """Test if filtered values are correctly recognized"""

    cfg = treedict.TreeDict()
    cfg.effect.s_bounds = ((-1.0, 1.0),)
    cfg.effect.s_res    = (10,)
    goalexplorer = effect.GridExplorer((1.0,), cfg = cfg)
    goalexplorer = effect.EffectFilter(goalexplorer, (((0.0, 0.0),),))

    return goalexplorer._in_filtered_values((0.0,)) and not goalexplorer._in_filtered_values((1.0,))

tests = [test_belongs]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))
