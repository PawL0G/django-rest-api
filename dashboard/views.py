from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView, DetailView

from .forms import IssueForm
from .models import Issue
from .services import get_issue, get_form, get_staff_from


def LikeView(request, pk):
    liked = False
    model = get_object_or_404(Issue, id=request.POST.get('issue_id'))

    if model.likes.filter(id=request.user.id).exists():
        model.likes.remove(request.user)
        liked = False
    else:
        model.likes.add(request.user)
        liked = True

    total_likes = model.likes.count()

    context = {
        "total_likes": total_likes
    }

    return HttpResponseRedirect(reverse('dashboard'), context)


class Dashboard(LoginRequiredMixin, ListView):
    template_name = "dashboard/dashboard.html"
    model = Issue
    login_url = reverse_lazy("login")

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.filter(user=self.request.user)

    # def get_context_data(self, *args, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(Dashboard, self).get_context_data(*args, **kwargs)
    #     # add whatever to your context:
    #     data = Issue.objects.all()
    #     total_likes = data.total_likes()
    #     context["total_likes"] = total_likes
    #     return context


class LikeList(DetailView):
    template_name = "dashboard/dashboard.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(LikeList).get_context_data(**kwargs)
        data = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = data.total_likes()
        context["total_likes"] = total_likes
        return context


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
