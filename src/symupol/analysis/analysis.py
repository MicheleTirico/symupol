from symupol.control.config import Config
from symupol.control.controller import Controller


class Analysis():
    def __init__(self,
                 config:Config,
                 controller=Controller):
        self.config=config
        self.controller=controller

    

    def test (self,val):
        print (val)

