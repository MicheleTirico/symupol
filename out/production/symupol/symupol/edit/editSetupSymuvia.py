import sys
import xml.etree.ElementTree as ET



class EditSetupSymuvia:
    def __init__(self, config):
        self.__config = config

        # tree scenario tmp
        self.__tree_scenarioTmp = ET.parse(self.__config.setupTmp)
        self.__root_scenarioTmp = self.__tree_scenarioTmp.getroot()

        # tree config
        self.__tree_config = ET.parse(self.__config.pathConfig)
        self.__root_config = self.__tree_config.getroot()


    def editSimulation(self, run):
        self.__config.logger.log(cl=self, method=sys._getframe(), message="create new setup, edit simulation")

        if run:
            simulation_config = self.__root_config.find("simulation")
            simulations_scenarioTmp = self.__root_scenarioTmp.find("SIMULATIONS")
            simulation_scenarioTmp = simulations_scenarioTmp.find("SIMULATION")
            for parameter in simulation_config:
                config_val = simulation_config.findall("./parameter[@name='" + parameter.attrib["name"] + "']")[0].text
                if config_val != None:
                    simulation_scenarioTmp.set(parameter.attrib["name"], simulation_config.findall(
                        "./parameter[@name='" + parameter.attrib["name"] + "']")[0].text)

            self.__tree_scenarioTmp.write(self.__config.setupTmp)

    def editRestitution(self, run):
        self.__config.logger.log(cl=self, method=sys._getframe(), message="create new setup, edit restitution")
        if self.__config.logger.warning(cl=self, method=sys._getframe(), message="method not implemented",doQuit=False,doReturn=True)==True: return

        if run:
            simulation_config = self.__root_config.find("restitution")
            simulations_scenarioTmp = self.__root_scenarioTmp.find("SIMULATIONS")
            simulation_scenarioTmp = simulations_scenarioTmp[0]
            for parameter in simulation_config:
                config_val = simulation_config.findall("./parameter[@name='" + parameter.attrib["name"] + "']")[0].text
                if config_val != None:
                    print (parameter.attrib["name"], simulation_config.findall(
                        "./parameter[@name='" + parameter.attrib["name"] + "']")[0].text)
                    simulation_scenarioTmp.set(parameter.attrib["name"], simulation_config.findall(
                        "./parameter[@name='" + parameter.attrib["name"] + "']")[0].text)

        self.__tree_scenarioTmp.write(self.__config.setupTmp)

    def editParametersTag(self,run,rootConfig,nameRoot,nameTag,message):
        self.__config.logger.log(cl=self, method=sys._getframe(), message=message)
        #if self.__config.logger.warning(cl=self, method=sys._getframe(), message="method not implemented",doQuit=False,doReturn=False)==True:            return
        list_edited_tag=[]
        if run:
            root_config = self.__root_config.find(rootConfig) # trafic
            root_scenarioTmp = self.__root_scenarioTmp.find(nameRoot) #TRAFICS
            tag_scenarioTmp = root_scenarioTmp.find(nameTag) #TRAFIC
            for parameter in root_config:
                config_val = root_config.findall("./parameter[@name='" + parameter.attrib["name"] + "']")[0].text
                if config_val != None:
                    tag_scenarioTmp.set(parameter.attrib["name"], root_config.findall(
                        "./parameter[@name='" + parameter.attrib["name"] + "']")[0].text)
                    list_edited_tag.append(parameter.attrib["name"])

            self.__config.logger.log(cl=self, method=sys._getframe(), message="file edited: "+str(list_edited_tag))
            self.__tree_scenarioTmp.write(self.__config.setupTmp)
