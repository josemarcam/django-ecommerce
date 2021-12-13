from django.urls import path
from . import views

app_name = "projects"   


urlpatterns = [
    path("", views.ListProject.as_view(), name="homepage"),
    path("<int:id>/", views.ProjectDetail.as_view(), name="details"),
    path("<int:id>/create/phase", views.CreateProjectPhase.as_view(), name="new_phase"),
]