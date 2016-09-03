from timeit import Timer


def test_this(func, args, env, number=100000):
    t = Timer("%s(%s)" % (func, args), "from __main__ import %s" % env)
    tm = t.timeit(number)
    return "%s: %10.03f" % (func, tm)
