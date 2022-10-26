
from django import forms


class FileSubmissionForm(forms.Form):
    file = forms.FileField(allow_empty_file=False)
