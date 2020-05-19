"""Entrypoint module, in case you use `python -m openbiolink`.

Why does this file exist, and why `__main__`? For more info, read:

 - https://www.python.org/dev/peps/pep-0338/
 - https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import openbiolink.globalConfig as glob
    glob.WORKING_DIR = r"C:\Users\sott\Desktop\testdelme"
    from openbiolink.evaluation.symbolic.symbolicEvaluation import AnyBURLEvaluation

    asdf = AnyBURLEvaluation("", "", "")

    from openbiolink.evaluation.metricTypes import RankMetricType

    asdf.evaluate(r"C:\Users\sott\Desktop\config-eval.properties", [RankMetricType.HITS_AT_K_REL], [1, 3, 10])
    #main()
