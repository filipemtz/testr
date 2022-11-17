from django.contrib import admin

from .models import (
    Course,
    Section,
    Question,
    EvaluationInputOutput,
    EvaluationScript,
    Submission,
    Enrollment,
    QuestionFile
)

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(EvaluationInputOutput)
admin.site.register(EvaluationScript)
admin.site.register(Submission)
admin.site.register(Enrollment)
admin.site.register(QuestionFile)
