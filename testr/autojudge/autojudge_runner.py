
import json
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
        report = judge.judge(submission, verbose)
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
