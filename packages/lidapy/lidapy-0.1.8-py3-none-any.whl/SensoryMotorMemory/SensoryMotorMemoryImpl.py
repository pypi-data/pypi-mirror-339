#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
import random

from src.ActionSelection.ActionSelection import ActionSelection
from src.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from src.Module.Initialization.DefaultLogger import getLogger
from src.SensoryMemory.SensoryMemory import SensoryMemory
from src.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self):
        super().__init__()
        self.action_event = None
        self.action_plan = None
        self.logger = getLogger(__class__.__name__).logger
        #self.logger.debug("Initialized SensoryMotorMemory")

    def run(self):
        self.logger.debug("Initialized SensoryMotorMemory")

    def notify(self, module):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        self.action_plan = []
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content(module)["cue"]
            iterations = random.randint(1, 5)
            index = 0
            for link in cue:
                if (link.getCategory("label") == "G" or
                        link.getCategory("label") == "F" or
                        link.getCategory("label") == "S"):
                    self.action_event = link.getCategory("id")
                    if index == iterations:
                        break
                    else:
                        index += 1
            if self.action_event is not None:
                self.notify_observers()
                self.logger.debug("Retrieved motor plan(s) from action plan")
                if isinstance(self.action_event, list):
                    for action in self.action_event:
                        self.action_plan.append(action)

        elif isinstance(module, ActionSelection):
            self.action_event = module.get_action()
            if self.action_event is not None:
                self.logger.debug("Retrieved motor plan(s) from action plan")
                if isinstance(self.action_event, list):
                    for action in self.action_event:
                        self.action_plan.append(action)
                self.notify_observers()

        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()

    def send_action_event(self):
        return self.action_event

    def send_action_execution_command(self):
        return self.action_plan