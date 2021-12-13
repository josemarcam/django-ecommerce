from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from activities.forms import NewActivityForm
from projects.models import Project, ProjectPhase
from activities.models import Activity
# Create your views here.

@login_required
# @permission_required('users.add_user',"users:homepage")
def new_activity_request(request, project_id:int, phase_id:int):
    project = Project.objects.filter(id = project_id).first()
    phase = ProjectPhase.objects.filter(id = phase_id).first()
    if request.method == "POST":
        request_post = request.POST
        form = NewActivityForm(request_post)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.creator = request.user
            activity.phase = phase
            activity.project = project
            activity.save()
            return redirect("projects:details", id=project_id)
    form = NewActivityForm()
    return render(request=request, template_name="activity/create_activity.html", context={"form":form, "project":project, "phase":phase})

@login_required
def activity_details_request(request,activity_id:int):
    activity = Activity.objects.filter(id=activity_id).first()
    return render(request=request, template_name="activity/activity_model_info.html", context={"activity":activity})