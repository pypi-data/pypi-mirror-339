import concurrent.futures
import glob
import importlib
from importlib import util
from pathlib import Path
from threading import Thread
from time import sleep
from yaml import YAMLError, safe_load

from Environment.Environment import Environment
from Environment.FrozenLakeEnvironment import FrozenLake
from Framework.Agents.Agent import Agent
from SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from Configs import Config


class MinimalReactiveAgent(Agent):
    def __init__(self):
        super().__init__()
        self.proj_path = Path.cwd()
        self.path = "Configs\module_locations.yaml"
        self.sensor_path = "Configs\DEFAULT_SENSORS.yaml"
        self.processor_path = "Configs\DEFAULT_PROCESSORS.yaml"
        self.environment_type = None

        # Agent modules
        self.environment = FrozenLake()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_from_module("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Module observers
        self.sensory_memory.add_observer(self.sensory_motor_mem)

        # Environment thread
        self.environment_thread = None

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.run_sensors))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.run))

        self.threads = [
            self.sensory_memory_thread,
            self.sensory_motor_mem_thread,
        ]

    def run(self):
        # Initialize environment dynamically
        self.environment = self.load_from_module(self.environment_type)

        if self.environment_type == "FrozenLakeEnvironment":
            self.environment_type = "FrozenLake"

        self.environment = self.environment.__getattribute__(
            self.environment_type)()
        self.environment.add_observer(self.sensory_memory)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.append(self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
            executor.shutdown(wait=True)

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            state = module.get_state()

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