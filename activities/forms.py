from django import forms

from activities.models import Activity


# Create your forms here.

class NewActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = [
            "name",
            "short_description",
            "description",
            "type",
            "cust",
        ]

    def save(self, commit=True):
        user = super(NewActivityForm, self).save(commit=False)
        if commit:
            user.save()
        return user