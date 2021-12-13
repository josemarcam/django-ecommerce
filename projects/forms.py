from django import forms

from projects.models import ProjectPhase


# Create your forms here.

class NewProjectPhaseForm(forms.ModelForm):

    class Meta:
        model = ProjectPhase
        fields = [
            "name",
            "description",
            "initial_budget",
            "start_date",
            "end_date",
            "is_current",
        ]

    def save(self, commit=True):
        phase = super(NewProjectPhaseForm, self).save(commit=False)
        if commit:
            phase.save()
        return phase