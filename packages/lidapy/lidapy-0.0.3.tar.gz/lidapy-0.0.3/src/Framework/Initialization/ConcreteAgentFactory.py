import glob
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
                return self.load_from_module(agent_type)
            except:
                raise ModuleNotFoundError(f"Module \"{agent_type}\" not found")

    def load_from_module(self, module):
        # Specify the module file path
        try:
            file_name = module + ".py"
            search_paths = ["C:\\Users\\*", "/home/*", "/*"]
            files = None
            for path in search_paths:
                files = glob.glob(f"{path}/**/{file_name}",
                                  recursive=True)
                if files:
                    break

            full_path = files[0]
        except Exception as exc:
            raise exc

        # Name the module
        module_name = module

        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
