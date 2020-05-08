"""Entrypoint module, in case you use `python -m openbiolink`.

Why does this file exist, and why `__main__`? For more info, read:

 - https://www.python.org/dev/peps/pep-0338/
 - https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

import logging
from .openBioLink import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import openbiolink.globalConfig as glob
    glob.WORKING_DIR = r"C:\Users\Simon\Desktop\testdelme"
    from openbiolink.evaluation.anyburl_evaluation import AnyBURLEvaluation

    asdf = AnyBURLEvaluation("", "", "")
    asdf.train("")
    #main()
