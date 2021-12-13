from django.urls import path
from . import views

app_name = "activities"   


urlpatterns = [
    path("create/<int:project_id>/<int:phase_id>/", views.new_activity_request, name="new_activity"),
    path("<int:activity_id>/", views.activity_details_request, name="details"),
]