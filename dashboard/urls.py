from django.urls import path
from .views import Dashboard, issue_page, ReportPage, search_page, Requirement, UpdateCommentVote

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("issue/<int:pk>", issue_page, name="issue"),
    path("report/", ReportPage.as_view(), name="report"),
    path("search/", search_page, name="search"),
    path("comments", Requirement.as_view(), name="requirements"),
    path("<int:comment_id>/<str:opition>", UpdateCommentVote.as_view(), name="requirement_comment_vote"),
]

