import os
from yaml import safe_load, YAMLError
import importlib.util

from Framework.Agents.Alarms_Control_Agent import AlarmsControlAgent
from Framework.Agents.Minimal_Reactive_Agent import MinimalReactiveAgent
from Framework.Agents.Minimal_Conscious_Agent import \
    MinimalConsciousAgent
from Framework.Initialization.AgentFactory import AgentFactory


class ConcreteAgentFactory(AgentFactory):
    # concrete factory for creating and initializing agents
    def __init__(self):
        super().__init__()

    def get_agent(self, agent_type):
        if agent_type == "MinimalReactiveAgent" or agent_type == 1:
            return MinimalReactiveAgent()
        elif agent_type == "AlarmsControlAgent" or agent_type == 2:
            return AlarmsControlAgent()
        elif agent_type == "MinimalConsciousAgent" or agent_type == 3:
            return MinimalConsciousAgent()
        else:
            try:
                return self.load_module_from_file(agent_type)
            except:
                raise ModuleNotFoundError(f"Module \"{agent_type}\" not found")

    def load_module_from_file(self, agent_type):
        with open("Configs/module_locations.yaml", "r") as yaml_file:
            try:
                loaded_module_locations = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)
        #Specify the module file path
        try:
            proj_path = os.path.dirname(os.path.abspath("lidapy"))
            module_path = loaded_module_locations[agent_type]
            full_path = proj_path + module_path
        except:
            raise KeyError(f"Invalid key \"{agent_type}\"")
        #Name the module
        module_name = agent_type

        #Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
