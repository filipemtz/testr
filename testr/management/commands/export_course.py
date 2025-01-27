


import os
import json
import datetime 

from shutil import rmtree
from tqdm import tqdm
from django.core.management.base import BaseCommand

from testr.models import *


class Command(BaseCommand):
    help = 'Copy the questions from a course to another.'

    def add_arguments(self, parser):
        parser.add_argument("id_in",
                            type=int,
                            help='Id of the input course.')

        parser.add_argument("output_directory",
                            type=str,
                            help='Path to the output directory in which the course will be saved.')

    def handle(self, *args, **options):
        out_dir = options['output_directory']

        if os.path.exists(out_dir):
            rmtree(out_dir)

        os.makedirs(out_dir)

        course_in = Course.objects.get(id=options['id_in'])

        course_json = {
            "name": course_in.name,
            "sections": [],
        }

        for section in tqdm(Section.objects.filter(course=course_in)):
            section_dir = os.path.join(out_dir, f"Section_{section.id:03d}")

            section_json = {"name": section.name, "questions": []}
            course_json['sections'].append(section_json) 

            for question in Question.objects.filter(section=section):
                
                question_json = { 
                    "name": question.name,
                    "description": question.description,
                    "language": question.language,
                    "time_limit_seconds": question.time_limit_seconds,
                    "memory_limit": question.memory_limit,
                    "cpu_limit": question.cpu_limit,
                    "submission_deadline": "2025/3/31 23:59:59",
                    "files": [],
                    "tests": []
                }
                section_json['questions'].append(question_json)

                question_dir = os.path.join(section_dir, f"Question_{question.id:03d}")

                os.makedirs(question_dir)

                for question_file in QuestionFile.objects.filter(question=question):
                    file_name = os.path.join(question_dir, question_file.file_name)
                    f = open(file_name, "wb")
                    f.write(question_file.file)
                    f.close()
                    question_json['files'].append(file_name)

                for in_out in EvaluationInputOutput.objects.filter(question=question):
                    test_json = {
                        "input": in_out.input,
                        "output": in_out.output
                    }

                    question_json['tests'].append(test_json)

        json_name = os.path.join(out_dir, "course.json")
        f = open(json_name, "w")
        json.dump(course_json, f)
        f.close()

        print("Done.")

