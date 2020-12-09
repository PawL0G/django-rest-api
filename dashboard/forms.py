from django import forms

from dashboard.models import Message, Issue


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = "__all__"
        exclude = ("priority", "user", "status")


class StaffEditIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ("priority", "status")
