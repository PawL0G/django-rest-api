from django.core.exceptions import ObjectDoesNotExist

from dashboard.forms import MessageForm, StaffEditIssueForm
from dashboard.models import Issue


def get_issue(pk):
    try:
        issue = Issue.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None

    return issue


def get_form(request, issue):
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(data=request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.issue = issue
            message.save()
            form = MessageForm()

    return form


def get_staff_from(post_data, issue):
    form = StaffEditIssueForm(instance=issue, data=post_data)

    if form.is_valid():
        form.save()

    return form
