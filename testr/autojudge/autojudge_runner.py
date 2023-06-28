
import json
from datetime import datetime

from testr.autojudge.cpp_judge import CppJudge
from testr.models.question import Language
from testr.models.submission import Submission, SubmissionStatus
from .base_judge import BaseJudge
from .python_judge import PythonJudge


class AutoJudgeRunner:
    judges = {
        Language.CCPP.value: CppJudge,
        Language.PYTHON.value: PythonJudge,
    }

    @classmethod
    def evaluate(cls,
                 submission: Submission,
                 keep_files: bool = False,
                 verbose: bool = False
                 ) -> None:

        judge_class = AutoJudgeRunner.judges[submission.question.language]

        judge = judge_class(keep_files)
        try:
            report = judge.judge(submission, verbose)
        except Exception as e:
            date_format = "%d/%m/%Y %H:%M:%S"
            dt = datetime.now().strftime(date_format)
            report = {
                "error_msgs": ["The submission crashed the autojudge."],
                "start_at": dt,
                "end_at": dt,
                "uuid": "",
                "input_output_test_report": {
                    "tests_reports": []
                }
            }

        report_json = json.dumps(report)
        submission.report_json = report_json

        if len(report["error_msgs"]) == 0:
            submission.status = SubmissionStatus.SUCCESS
        else:
            submission.status = SubmissionStatus.FAIL

        submission.save()

        if verbose:
            print("--------------------------")

        print(
            f"Submission {report['uuid']}: {submission} evaluated with {submission.status.label}.")

        if verbose:
            print("--------------------------")

        if verbose and (len(report["error_msgs"]) > 0):
            print("Error messages:")
            print("--------------------------")
            for msg in report["error_msgs"]:
                print("* ", msg)
            print("--------------------------")

    @classmethod
    def register_judge(cls, language: str, judge_class: BaseJudge) -> None:
        AutoJudgeRunner.judges[language] = judge_class
