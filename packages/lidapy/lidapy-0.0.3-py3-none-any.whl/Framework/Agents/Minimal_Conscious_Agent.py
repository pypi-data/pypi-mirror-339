import concurrent.futures
import glob
import importlib
from importlib import util
from pathlib import Path
from threading import Thread
from time import sleep
from yaml import YAMLError, safe_load


from ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from AttentionCodelets.AttentionCodeletImpl import AttentionCodeletImpl
from Environment.Environment import Environment
from Framework.Agents.Agent import Agent
from GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from PAM.PAM_Impl import PAMImpl
from ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from Workspace.CurrentSituationalModel.CurrentSituationalModelImpl import \
    CurrentSituationalModelImpl
from Workspace.WorkspaceImpl import WorkspaceImpl
from Configs import Config


class MinimalConsciousAgent(Agent):
    def __init__(self):
        super().__init__()
        self.proj_path = Path.cwd()
        self.path = r"Configs\module_locations.yaml"
        self.sensor_path = r"Configs\DEFAULT_SENSORS.yaml"
        self.processor_path = r"Configs\DEFAULT_PROCESSORS.yaml"
        self.environment_type = None

        #Agent modules
        self.environment = None
        self.global_workspace = GlobalWorkSpaceImpl()
        self.csm = CurrentSituationalModelImpl()
        self.attention_codelets = AttentionCodeletImpl()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.workspace = WorkspaceImpl()
        self.sensory_memory = SensoryMemoryImpl()

        #Module observers
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.attention_codelets.add_observer(self.csm)
        self.pam.add_observer(self.procedural_memory)
        self.pam.add_observer(self.workspace)
        self.procedural_memory.add_observer(self.action_selection)
        self.workspace.add_observer(self.pam)
        self.sensory_memory.add_observer(self.csm)
        self.sensory_memory.add_observer(self.pam)
        self.sensory_memory.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.pam)
        self.global_workspace.add_observer(self.procedural_memory)
        self.global_workspace.add_observer(self.action_selection)
        self.global_workspace.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.attention_codelets)
        self.csm.add_observer(self.global_workspace)

        #Global Workspace Ticks
        self.global_workspace.ticks = 0

        #Add workspace csm
        self.workspace.csm = self.csm

        #Add attention codelets buffer
        self.attention_codelets.buffer = self.csm

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        #Environment thread
        self.environment_thread = None

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_from_module("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.run_sensors))

        # PAM thread
        self.pam_thread = Thread(target=self.pam.run)

        # Workspace thread
        self.workspace_thread = Thread(target=self.workspace.run)

        # CSM thread
        self.csm_thread = Thread(target=self.csm.run_task)

        # Attention codelets thread
        self.attention_codelets_thread = Thread(
            target=self.attention_codelets.start)

        # GlobalWorkspace thread
        self.global_workspace_thread = (
            Thread(target=self.global_workspace.run_task))

        # ProceduralMem thread
        self.procedural_memory_thread = (
            Thread(target=self.procedural_memory.run,
                    args=(["Avoid hole", "Find goal"],)))

        # ActionSelection thread
        self.action_selection_thread = (
            Thread(target=self.action_selection.run))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.run))

        self.threads = [
            self.sensory_memory_thread,
            self.csm_thread,
            self.attention_codelets_thread,
            self.pam_thread,
            self.workspace_thread,
            self.global_workspace_thread,
            self.procedural_memory_thread,
            self.action_selection_thread,
            self.sensory_motor_mem_thread,
        ]


    def run(self):
        #Initialize environment dynamically
        self.environment = self.load_from_module(self.environment_type)
        if self.environment_type == "FrozenLakeEnvironment":
            self.environment_type = "FrozenLake"

        self.environment = self.environment.__getattribute__(
                                                    self.environment_type)()
        self.environment.add_observer(self.sensory_memory)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.insert(0, self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
            executor.shutdown(wait=True, cancel_futures=False)

        if self.get_state()["done"]:
            self.global_workspace.task_manager.set_shutdown(True)
            self.attention_codelets.shutdown = True

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            stimuli = module.get_stimuli()

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

    def get_agent_sensors(self):
        try:
            DEFAULT_SENSORS = Config.DEFAULT_SENSORS
            return DEFAULT_SENSORS
        except Exception as exc:
            print(exc)

    def get_agent_processors(self):
        try:
            DEFAULT_PROCESSORS = Config.DEFAULT_PROCESSORS
            return DEFAULT_PROCESSORS
        except YAMLError as exc:
            print(exc)

    def get_state(self):
        return self.environment.get_state()