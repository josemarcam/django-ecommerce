from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from django.shortcuts import redirect, render
from projects.models import Project, ProjectUser
from django.db.models import Q
from datetime import date
from projects.forms import NewProjectPhaseForm

class ListProject(LoginRequiredMixin,ListView):
    
    model = ProjectUser
    template_name = "projects/my_projects.html"
    context_object_name = "projects"

    def get_queryset(self, **kwargs):
        return ProjectUser.objects.filter(user = self.request.user).all()

class ProjectDetail(LoginRequiredMixin,DetailView):
    
    model = ProjectUser
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_queryset(self):
        criterion1 = Q(user = self.request.user.id)
        return self.model.objects.filter(criterion1)

class CreateProjectPhase(FormView):
    
    form_class = NewProjectPhaseForm
    template_name = "projects/create_phase.html"

    def form_valid(self, form):
        project = Project.objects.filter(id = self.kwargs['id']).first()
        phase = form.save(commit=False)
        phase.project = project
        phase.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        project = Project.objects.filter(id = self.kwargs['id']).first()
        return project.get_absolute_url()

# @login_required
# def list_project_request(request):
    
#     user = request.user
#     projects = ProjectUser.objects.filter(user = user.id).all()
        
#     return render(request=request, template_name="projects/my_projects.html", context={"projects":projects})

# @login_required
# def project_detail_request(request,id:int):
    
#     user = request.user
#     criterion1 = Q(user = user.id)
#     criterion2 = Q(project = id)

#     project = ProjectUser.objects.filter(criterion1 & criterion2).first().project
    # days_to_end = project.end_date - date.today()
    # print(str(days_to_end))
    
    # return render(request=request, template_name="projects/project_detail.html", context={"project":project})

# @login_required
# def new_project_phase(request,id:int):
#     project = Project.objects.filter(id = id).first()
#     if request.method == "POST":
#         request_post = request.POST
#         form = NewProjectPhaseForm(request_post)
#         if form.is_valid():
#             phase = form.save(commit=False)
#             phase.project = project
#             phase.save()
#             return redirect("projects:details", id=id)
#     form = NewProjectPhaseForm()
#     return render(request=request, template_name="projects/create_phase.html", context={"form":form, "project":project})