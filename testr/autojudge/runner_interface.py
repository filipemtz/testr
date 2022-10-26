
from abc import ABC, abstractmethod
from typing import Dict, Any


class RunnerInterface(ABC):
    @abstractmethod
    def run(self, input_value) -> Dict[str, Any]:
        """ Run a command for a given input and return a dictionary with 
            the result of the run. """
