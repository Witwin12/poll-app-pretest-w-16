from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("pivate/", views.pirvate_polls.as_view(), name='pivate'),
    path("pivate/<int:pk>/", views.PirvateDetailView.as_view(), name="pivatedetail"),
    path("pivate/<int:pk>/results/", views.PirvateResultsView.as_view(), name="pivateresults"),
]