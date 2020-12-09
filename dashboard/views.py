from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from .forms import IssueForm, CommentForm
from .models import Issue, Comment, Like, DisLike
from .services import get_issue, get_form, get_staff_from


class Dashboard(LoginRequiredMixin, ListView):
    template_name = "dashboard/dashboard.html"
    model = Issue
    login_url = reverse_lazy("login")

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.filter(user=self.request.user)


def search_page(request):
    username = request.GET.get("username", None)
    if username:
        users = User.objects.filter(username__contains=username)
        issue_list = Issue.objects.filter(user__in=users)
        context = {
            "issue_list": issue_list,
        }
    else:
        context = {}

    return render(request, "dashboard/dashboard.html", context)


def issue_page(request, pk):
    issue = get_issue(pk)
    form = get_form(request, issue)

    if request.user.is_staff:
        staff_form = get_staff_from(request.POST, issue)
    else:
        staff_form = None

    if issue.user == request.user or request.user.is_staff:
        if not issue:
            return HttpResponseNotFound()

        context = {
            "issue": issue,
            "form": form,
            "staff_form": staff_form,
        }

        return render(request, 'dashboard/issue.html', context)

    return HttpResponseForbidden()


class ReportPage(FormView):
    template_name = 'dashboard/report.html'
    form_class = IssueForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.user = self.request.user
        issue.save()

        return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin


class Requirement(View):
    form_class = CommentForm
    template_name = 'dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        comment = Comment.objects.all()

        context = {}
        context['page_obj'] = comment
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = request.user
            comment_form.save()
            messages.success(request, 'Your comment successfully addedd')

            return HttpResponseRedirect(reverse_lazy('comment'))

        context = {}
        context['form'] = form

        return render(request, self.template_name, context)


class UpdateCommentVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):

        comment_id = self.kwargs.get('comment_id', None)
        opition = self.kwargs.get('opition', None)  # like or dislike button clicked

        comment = get_object_or_404(Comment, id=comment_id)

        try:
            # If child DisLike model doesnot exit then create
            comment.dis_likes
        except Comment.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment=comment)

        try:
            # If child Like model doesnot exit then create
            comment.likes
        except Comment.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(comment=comment)

        if opition.lower() == 'like':

            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse_lazy('comment'))
        return HttpResponseRedirect(reverse_lazy('comment'))
