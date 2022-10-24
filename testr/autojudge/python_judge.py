
import glob
from typing import Tuple
from pathlib import Path
from .base_judge import BaseJudge


class PythonJudge(BaseJudge):
    def _evaluate_files_and_prepare_executable(self) -> Tuple[str, bool]:
        files = glob.glob(f"{self.test_dir}/**/*.py", recursive=True)

        if len(files) <= 0:
            # python file not found
            self.report["error_msgs"].append("Python file not found.")
            return '', False
        elif len(files) == 1:
            # if there is only one python file, assume it is the correct
            p = self._clean_program_name(files[0], self.test_dir)
            return f"python {p}", True
        else:
            # search for a main.py file.
            main_files = []
            for f in files:
                if Path(f).name == 'main.py':
                    main_files.append(f)

            if len(main_files) == 1:
                p = self._clean_program_name(main_files[0], self.test_dir)
                return f"python {p}", True

            # search for the one with __main__.
            runnable_files = []
            for f in files:
                with open(f, "r") as f:
                    file_content = f.read()

                if "__main__" in file_content:
                    runnable_files.append(f)

            if len(runnable_files) == 1:
                p = self._clean_program_name(runnable_files[0], self.test_dir)
                return f"python {p}", True

            self.report["error_msgs"].append(
                "Python files were found, but autojudge could not figure out "
                "which one it should run. Try renaming the executable as "
                "'main.py'."
            )

            return "", False

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
