from django.contrib import admin
from projects.models import Project, ProjectPhase, ProjectUser

class ProjectUserInline(admin.TabularInline):
    model = ProjectUser
    extra = 1

class ProjectPhaseInline(admin.TabularInline):
    model = ProjectPhase
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    inlines = (ProjectUserInline,ProjectPhaseInline)
    
    list_display = [
        "name",
        "is_started",
        "is_ended",
        "start_date",
        "end_date",
        "initial_budget",
    ]
    list_filter = ["is_started", "is_ended", "start_date", "end_date", "created", "modified"]
    list_editable = ["is_started","is_ended","start_date","end_date"]

@admin.register(ProjectPhase)
class ProjectPhaseAdmin(admin.ModelAdmin):
    
    list_display = [
        "name",
        "initial_budget",
        "is_current",
    ]
    list_filter = ["name", "is_current"]