

import datetime 

from tqdm import tqdm
from django.core.management.base import BaseCommand

from testr.models import *


class Command(BaseCommand):
    help = 'Copy the questions from a course to another.'

    def add_arguments(self, parser):
        parser.add_argument("id_in",
                            type=int,
                            help='Id of the input course.')

        parser.add_argument("id_out",
                            type=int,
                            help='Id of the output course.')

    def handle(self, *args, **options):
        course_in = Course.objects.get(id=options['id_in'])
        course_out = Course.objects.get(id=options['id_out'])      

        # !! Remove all sections from the the output course
        Section.objects.filter(course=course_out).delete()

        for section in tqdm(Section.objects.filter(course=course_in)):
            new_section = Section(course=course_out, name=section.name)
            new_section.save()

            for question in Question.objects.filter(section=section):
                new_question = Question(section=new_section,
                        name=question.name,
                        description=question.description,
                        language=question.language,
                        time_limit_seconds=question.time_limit_seconds,
                        memory_limit=question.memory_limit,
                        cpu_limit=question.cpu_limit,
                        submission_deadline=datetime.datetime(2025, 3, 31, 23, 59, 59))

                new_question.save()

                for question_file in QuestionFile.objects.filter(question=question):
                    new_file = QuestionFile(question=new_question,
                            file=question_file.file,
                            file_name=question_file.file_name)

                    new_file.save()


                for in_out in EvaluationInputOutput.objects.filter(question=question):
                    new_io = EvaluationInputOutput(question=new_question,
                            input=in_out.input,
                            output=in_out.output)

                    new_io.save()

        print("Done.")

