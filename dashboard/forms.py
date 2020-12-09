from django import forms

from dashboard.models import Message, Issue, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
