from symupol.analysis.analysis import Analysis
from symupol.analysis.test import Test
from symupol.control.config import Config

c=Config("")
a = Analysis(config=c)
t=Test(a)
a.test(3)
