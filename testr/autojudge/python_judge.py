
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
            return f"python {files[0]}", True
        else:
            # search for a main.py file.
            main_files = []
            for f in files:
                if Path(f).name == 'main.py':
                    main_files.append(f)

            if len(main_files) == 1:
                return f"python {main_files[0]}", True

            # search for the one with __main__.
            runnable_files = []
            for f in files:
                with open(f, "r") as f:
                    file_content = f.read()

                if "__main__" in file_content:
                    runnable_files.append(f)

            if len(runnable_files) == 1:
                return f"python {runnable_files[0]}", True

            self.report["error_msgs"].append(
                "Python files were found, but autojudge could not figure out "
                "which one it should run. Try renaming the executable as "
                "'main.py'."
            )

            return "", False
