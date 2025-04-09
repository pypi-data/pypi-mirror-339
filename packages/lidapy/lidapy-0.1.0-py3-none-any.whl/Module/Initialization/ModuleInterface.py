from abc import ABC, abstractmethod
from src.Module.ModuleSubject import ModuleSubject
from src.Module.ModuleObserver import ModuleObserver


class Module(ModuleObserver, ModuleSubject, ABC):

    @abstractmethod
    def notify(self, module):
        pass
