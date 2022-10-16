

import uuid
from time import sleep
from django.core.management.base import BaseCommand
from codetest.autojudge.autojudge_runner import AutoJudgeRunner
from codetest.models.submission import Submission, SubmissionStatus


class Command(BaseCommand):
    help = 'Judge submissions.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rerun',
            action='store_true',
            help='Use this option to evaluate all submissions again.')

        parser.add_argument(
            '--keep',
            action='store_true',
            help='Prevent deletion of files in autojudge directory.')

    def handle(self, *args, **options):
        if options['rerun']:
            Submission.objects.update(
                status=SubmissionStatus.WAITING_EVALUATION)

        while True:

            submissions = Submission.objects.filter(
                status=SubmissionStatus.WAITING_EVALUATION)

            if submissions.count() == 0:
                print(
                    "No submissions without evaluation were found. Sleeping for 5 seconds.")
                sleep(5)
            else:
                # last is selected because by default submissions are ordered by
                # submission time, with the most recent first.
                selected_submission = submissions.first()
                AutoJudgeRunner.evaluate(selected_submission, options['keep'])
