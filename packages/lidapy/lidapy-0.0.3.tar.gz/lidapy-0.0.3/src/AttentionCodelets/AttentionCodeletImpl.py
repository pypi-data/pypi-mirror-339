import time
from time import sleep

from AttentionCodelets.AttentionCodelet import AttentionCodelet
from GlobalWorkspace.CoalitionImpl import CoalitionImpl
from GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from Module.Initialization.DefaultLogger import getLogger
from Workspace.CurrentSituationalModel.CurrentSituationalModelImpl import \
    CurrentSituationalModelImpl

DEFAULT_CODELET_REFRACTORY_PERIOD = 50
DEFAULT_CODELET_REINFORCEMENT = 0.5
DEFAULT_CODELET_REMOVAL_THRESHOLD = -1.0
DEFAULT_CODELET_ACTIVATION = 1.0

class AttentionCodeletImpl(AttentionCodelet):
    def __init__(self):
        super().__init__()
        self.buffer = None
        self.global_workspace = None
        self.codeletRefractoryPeriod = DEFAULT_CODELET_REFRACTORY_PERIOD
        self.formed_coalition = None
        self.codelet_reinforcement = DEFAULT_CODELET_REINFORCEMENT
        self.shutdown = False
        self.logger = getLogger(self.__class__.__name__).logger
        self.logger.debug("Initialized attention codelets")

    def start(self):
        self.logger.debug("Running attention codelets")
        self.run_task()

    def run_task(self):
        if self.bufferContainsSoughtContent(self.buffer):
            csm_content = self.retrieveWorkspaceContent(
                                    self.buffer)
            if csm_content is None:
                self.logger.warning("Null WorkspaceContent returned."
                                          "Coalition cannot be formed.")
            elif csm_content.getLinkCount() > 0:
                self.formed_coalition = CoalitionImpl()
                self.formed_coalition.setContent(csm_content)
                self.formed_coalition.setCreatingAttentionCodelet(self)
                self.formed_coalition.setActivation(1.0)
                self.logger.info("Coalition successfully formed.")
                self.notify_observers()
                while not self.shutdown:
                    sleep(25)
                    self.run_task()
            else:
                while csm_content.getLinkCount() == 0:
                    time.sleep(10)
                self.run_task()

    def set_refactory_period(self, ticks):
        if ticks > 0:
            self.codeletRefractoryPeriod = ticks
        else:
            self.codeletRefractoryPeriod =  (
                DEFAULT_CODELET_REFRACTORY_PERIOD)

    def get_refactory_period(self):
        return self.codeletRefractoryPeriod

    def notify(self, module):
        if isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.__getstate__()
            self.learn(winning_coalition)

    def learn(self, coalition):
        global coalition_codelet
        if isinstance(coalition, CoalitionImpl):
            coalition_codelet = coalition.getCreatingAttentionCodelet()
        if isinstance (coalition_codelet, AttentionCodelet):
            newCodelet = AttentionCodeletImpl()
            newCodelet.buffer = self.buffer
            content = coalition.getContent()
            newCodelet.setSoughtContent(content)
            newCodelet.run_task()
            self.logger.debug(f"Created new codelet: {newCodelet}")
        elif coalition_codelet is not None:
    # TODO Reinforcement amount might be a function of the broadcast's
    # activation
            #coalition_codelet.reinforceBaseLevelActivation(
                #self.codelet_reinforcement)
            self.logger.debug(f"Reinforcing codelet: {coalition_codelet}")

    def getModuleContent(self):
        return self.formed_coalition

    def bufferContainsSoughtContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModelImpl):
            if buffer.getBufferContent() is not None:
                return True
        return False

    """
        Returns sought content and related content from specified
        WorkspaceBuffer
        """
    def retrieveWorkspaceContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModelImpl):
            return buffer.getBufferContent()

