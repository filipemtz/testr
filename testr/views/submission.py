
import json
from typing import Any, Dict
from django.views import generic
from testr.models import Submission
from testr.models.submission import SubmissionStatus
from testr.utils.group_validator import GroupValidator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


class SubmissionDetailView(generic.DetailView):
    model = Submission

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['error_msgs'] = []
        context['submission_uuid'] = '-'

        if self.object.status != SubmissionStatus.WAITING_EVALUATION:
            report = json.loads(self.object.report_json)
            report['error_msgs'] = [
                e.replace("\n", "<br>") for e in report['error_msgs']]

            context['submission_uuid'] = report['uuid']
            context['error_msgs'] = report['error_msgs']

        return context


class SubmissionDelete(DeleteView):
    model = Submission

    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={
            "pk": self.object.question.id
        })


def submission_get_file(request, pk):
    submission = get_object_or_404(Submission, id=pk)
    data = submission.file
    name = submission.file_name

    if (submission.student != request.user) and (not GroupValidator.user_is_in_group(request.user, 'teacher')):
        return HttpResponse('Unauthorized', status=401)

    content_type = 'text/plain'
    if '.zip' in name:
        content_type = 'multipart/form-data'

    name = f"Q{submission.question.id:05d}_{submission.student.username}_{submission.student.first_name}_{name}"

    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={name}'

    return response
