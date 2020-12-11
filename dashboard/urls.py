from django.urls import path
from .views import Dashboard, issue_page, ReportPage, search_page, LikeView, LikeList

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("issue/<int:pk>", issue_page, name="issue"),
    path("report/", ReportPage.as_view(), name="report"),
    path("search/", search_page, name="search"),
    path("like/<int:pk>", LikeView, name="issue_likes"),
    path('<int:pk>/', LikeList.as_view(), name='detail'),
]
