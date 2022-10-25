
import os
from glob import glob
from typing import Tuple
from pathlib import Path

from testr.autojudge.docker_runner import DockerRunner, UnsafeRunner
from .base_judge import BaseJudge


class CppJudge(BaseJudge):
    SRC_PTRN = ['*.c', '*.cc', '*.cpp']
    MAKE_PTRN = ['makefile', 'Makefile']
    HEADER_PTRN = ["*.h", "*.hpp"]
    IGNORE_PTRN = [".o", ".a", ".so"]

    def _get_files_with_patterns(self, patterns):
        files = []
        for p in patterns:
            files.extend(glob(f"{self.test_dir}/**/{p}", recursive=True))
        return files

    def _evaluate_files_and_prepare_executable(self) -> Tuple[str, bool]:
        self.src_files = self._get_files_with_patterns(CppJudge.SRC_PTRN)
        self.makefiles = self._get_files_with_patterns(CppJudge.MAKE_PTRN)

        if len(self.src_files) <= 0:
            # source files not found.
            self.report["error_msgs"].append("C/C++ files not found.")
            return '', False

        # if the source is inside some dir, change to this directory
        first_dir = self._find_first_directory(self.src_files + self.makefiles)
        self.test_dir = first_dir

        compilation_cmd = self._get_compilation_command()

        # make with docker and check for compilation errors
        runner = UnsafeRunner(
            compilation_cmd,
            timeout_seconds=120,
        )

        '''
        runner = DockerRunner(
            compilation_cmd,
            timeout_seconds=120,
            docker_dir=f"/submissions/{self.test_uuid}/",
            host_dir=self.test_dir
        )
        '''

        result = runner.run()

        if result['time_limit_exceeded']:
            self.report["error_msgs"].append("Compilation timeout.")
            return '', False

        if (result['result'].stdout.strip() != '') or \
            (result['result'].stderr.strip() != '') or \
                (result['result'].returncode != 0):

            msg = result['result'].stdout
            msg += "<br>"
            msg += result['result'].stderr
            msg += "<br>"

            self.report["error_msgs"].append(
                f"Compilation error: <br> {msg}.")

            return '', False

        # run the program with docker and check for runtime errors
        headers = self._get_files_with_patterns(CppJudge.HEADER_PTRN)
        binaries = self._get_files_with_patterns(CppJudge.IGNORE_PTRN)
        known_files = self.src_files + self.makefiles + headers + binaries

        all_files = glob(f"{self.test_dir}/**/*", recursive=True)
        executables = [f for f in all_files if f not in known_files]

        if len(executables) == 0:
            self.report["error_msgs"].append(
                f"Compilation seems to have succeeded, but executable was not found.")
            return '', False
        elif len(executables) > 1:
            self.report["error_msgs"].append(
                f"More than one executable candidate was found: '{executables}'. Update the makefile to generate a single executable.")
            return '', False

        return executables[0], True

    def _get_compilation_command(self):
        if len(self.makefiles) >= 0:
            lst = os.listdir(self.test_dir)
            makefile_found = False
            for ptrn in CppJudge.MAKE_PTRN:
                if ptrn in lst:
                    makefile_found = True
                    break

            # TODO: add an warning informating that makefiles were found,
            # but none of them is in the project root.

            if makefile_found:
                return "make"

        cc = self.config['cpp']['cc']
        flags = self.config['cpp']['flags']
        src = ' '.join(self.src_files)
        executable = os.path.join(self.test_dir, 'main')

        return f"{cc} {src} {flags} -o {executable}"

    def _find_first_directory(self, files):
        # assume the first directory is the one with smaller name
        # the following sort the files dirs by their size in descending order and return the first
        dirs = [str(Path(f).parent) for f in files]
        return list(sorted(dirs, key=lambda x: len(x), reverse=True))[0]

    def _clean_program_name(self, program_name, test_dir):
        # we remove the run directory because docker will add it later.
        # TODO: the replace in self.test_dir is already performed later in
        # base_judge.py:judge(). Improve this.
        d = str(test_dir).replace("\\", "/")
        p = program_name.replace("\\", "/")

        if p.find(d) == -1:
            raise Exception(
                f"Directory '{d}' not found in program path '{p}'.")

        p = p[len(d):]
        p = p.strip("/")

        return p
