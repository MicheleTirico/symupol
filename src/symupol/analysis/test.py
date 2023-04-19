from symupol.analysis.analysis import Analysis

class Test():
    def __init__(self,analysis):
        self.val=2
        print (analysis.config)
        analysis.test(3)
