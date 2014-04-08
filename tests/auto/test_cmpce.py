import testenv
import forest

from goals.explorer.tools import cmpce

def test1():
    """Test basic method of competence"""
    check = True

    cfg = forest.Tree()

    cfg.cmpce.min_d     = 0.01
    cfg.cmpce.function  = 'ident'
    cmpce.competence([1.0], [0.5], cfg)

    cfg.cmpce.exp_alpha = 3.0
    cfg.cmpce.function  = 'exp'
    cmpce.competence([1.0], [0.5], cfg)

    cfg.cmpce.log_beta  = 0.1
    cfg.cmpce.function  = 'log'
    cmpce.competence([1.0], [0.5], cfg)

    check *= cmpce.competence([0.01], [0.005], cfg) == 0.0


    return check


tests = [test1]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))