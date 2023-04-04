from symupy.runtime.api import Simulator, Simulation
import os

scenario = os.path.abspath("/home/mt_licit/project/symupol/scenarios/test_grid_01/5x5grid.xml")

s=Simulator()

s.register_simulation(scenario)

s.run()