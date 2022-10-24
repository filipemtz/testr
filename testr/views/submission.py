
import json
from typing import Any, Dict
from django.views import generic
from testr.models import Submission
from testr.models.submission import SubmissionStatus
from django.shortcuts import get_object_or_404, redirect


class SubmissionDetailView(generic.DetailView):
    model = Submission

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['error_msgs'] = []
        context['submission_uuid'] = '-'

        if self.object.status != SubmissionStatus.WAITING_EVALUATION:
            report = json.loads(self.object.report_json)
            context['submission_uuid'] = report['uuid']
            context['error_msgs'] = report['error_msgs']

        return context
