import os
import time
import subprocess
from typing import List, Optional
from testr.autojudge.runner_interface import RunnerInterface


class UnsafeRunner(RunnerInterface):
    # TODO: support cpu and memory limits.
    def __init__(self,
                 command: str,
                 timeout_seconds: Optional[float] = None,
                 running_dir: Optional[str] = None
                 ):

        self._command = command
        self._timeout_seconds = timeout_seconds
        self._running_dir = running_dir

        if not self._running_dir:
            self._running_dir = os.getcwd()

    def run(self, input_str: str = '', discard_outputs: List[str] = [], verbose: bool = False):
        start = time.time()
        result = None
        time_limit_exceeded = False

        if verbose:
            print("--------------------------")
            print(f"Running command")
            print(f"*** Command: {self._command}")
            print(f"*** Input: {input_str}")

        try:
            # see https://docs.python.org/3/library/subprocess.html
            result = subprocess.run(
                self._command,
                input=input_str,
                capture_output=True,
                shell=True,
                text=True,
                cwd=self._running_dir,
                timeout=self._timeout_seconds
            )

            # when running with docker, we use the timeout function that returns
            # error 124 when the program takes longer to finish than than the
            # given time.
            if result.returncode == 124:
                time_limit_exceeded = True

            for o in discard_outputs:
                result.stdout = result.stdout.replace(o, "")
                result.stderr = result.stderr.replace(o, "")

            result.stdout = result.stdout.strip()
            result.stderr = result.stderr.strip()

        except subprocess.TimeoutExpired:
            time_limit_exceeded = True

        end = time.time()

        report = {
            "command": self._command,
            "input": input_str,
            "result": result,
            "time_limit_exceeded": time_limit_exceeded,
            "running_time": (end - start)
        }

        if verbose:
            if time_limit_exceeded:
                print("*** Timeout")
            else:
                print("*** Result: ", result)
            print("--------------------------")

        return report
